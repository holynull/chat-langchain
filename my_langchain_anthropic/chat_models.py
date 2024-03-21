import os
import re
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Tuple, Union

import anthropic
from langchain_core._api.deprecation import deprecated
from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import (
    BaseChatModel,
    agenerate_from_stream,
    generate_from_stream,
)
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    ToolMessage,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.pydantic_v1 import Field, SecretStr, root_validator
from langchain_core.utils import (
    build_extra_kwargs,
    convert_to_secret_str,
    get_pydantic_field_names,
)
import json

_message_type_lookups = {
    "human": "user",
    "ai": "assistant",
    "AIMessageChunk": "assistant",
    "tool": "user",
}


def _format_image(image_url: str) -> Dict:
    """
    Formats an image of format data:image/jpeg;base64,{b64_string}
    to a dict for anthropic api

    {
      "type": "base64",
      "media_type": "image/jpeg",
      "data": "/9j/4AAQSkZJRg...",
    }

    And throws an error if it's not a b64 image
    """
    regex = r"^data:(?P<media_type>image/.+);base64,(?P<data>.+)$"
    match = re.match(regex, image_url)
    if match is None:
        raise ValueError(
            "Anthropic only supports base64-encoded images currently."
            " Example: data:image/png;base64,'/9j/4AAQSk'..."
        )
    return {
        "type": "base64",
        "media_type": match.group("media_type"),
        "data": match.group("data"),
    }


def _format_messages(messages: List[BaseMessage]) -> Tuple[Optional[str], List[Dict]]:
    """Format messages for anthropic."""

    """
    [
                {
                    "role": _message_type_lookups[m.type],
                    "content": [_AnthropicMessageContent(text=m.content).dict()],
                }
                for m in messages
            ]
    """
    system: Optional[str] = None
    formatted_messages: List[Dict] = []
    for i, message in enumerate(messages):
        if message.type == "system":
            if i != 0:
                raise ValueError("System message must be at beginning of message list.")
            if not isinstance(message.content, str):
                raise ValueError(
                    "System message must be a string, "
                    f"instead was: {type(message.content)}"
                )
            system = message.content
            continue

        # role = _message_type_lookups[message.type]
        _role = getattr(message, "role", None)
        role = _role if _role != None else _message_type_lookups[message.type]
        content: Union[str, List[Dict]]

        if not isinstance(message.content, str):
            # parse as dict
            assert isinstance(
                message.content, list
            ), "Anthropic message content must be str or list of dicts"

            # populate content
            content = []
            for item in message.content:
                if isinstance(item, str):
                    content.append(
                        {
                            "type": "text",
                            "text": item,
                        }
                    )
                elif isinstance(item, dict):
                    if "type" not in item:
                        raise ValueError("Dict content item must have a type key")
                    if item["type"] == "image_url":
                        # convert format
                        source = _format_image(item["image_url"]["url"])
                        content.append(
                            {
                                "type": "image",
                                "source": source,
                            }
                        )
                    else:
                        content.append(item)
                else:
                    raise ValueError(
                        f"Content items must be str or dict, instead was: {type(item)}"
                    )
        else:
            if isinstance(message, ToolMessage):
                content = f"""
<function_results>
    <result>
        <tool_name>{message.additional_kwargs["name"]}</tool_name>
        <stdout>
            {message.content}
        </stdout>
    </result>
</function_results>
"""
            elif isinstance(message, AIMessageChunk):
                content = message.additional_kwargs["xml_text"]
            else:
                content = message.content

        formatted_messages.append(
            {
                "role": role,
                "content": content,
            }
        )
    return system, formatted_messages


SEARCH_FUNCTION_CALL_SIZE = 20


class ChatAnthropic(BaseChatModel):
    """Anthropic chat model.

    To use, you should have the packages ``anthropic`` and ``langchain-anthropic``
    installed, and the environment variable ANTHROPIC_API_KEY set with your API key,
    or pass it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_anthropic import ChatAnthropic

            model = ChatAnthropic()
    """

    class Config:
        """Configuration for this pydantic object."""

        allow_population_by_field_name = True

    _client: anthropic.Client = Field(default=None)
    _async_client: anthropic.AsyncClient = Field(default=None)

    model: str = Field(alias="model_name")
    """Model name to use."""

    max_tokens: int = Field(default=1024, alias="max_tokens_to_sample")
    """Denotes the number of tokens to predict per generation."""

    temperature: Optional[float] = None
    """A non-negative float that tunes the degree of randomness in generation."""

    top_k: Optional[int] = None
    """Number of most likely tokens to consider at each step."""

    top_p: Optional[float] = None
    """Total probability mass of tokens to consider at each step."""

    default_request_timeout: Optional[float] = None
    """Timeout for requests to Anthropic Completion API. Default is 600 seconds."""

    anthropic_api_url: str = "https://api.anthropic.com"

    anthropic_api_key: Optional[SecretStr] = None

    model_kwargs: Dict[str, Any] = Field(default_factory=dict)

    streaming: bool = False
    """Whether to use streaming or not."""

    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "anthropic-chat"

    @root_validator(pre=True)
    def build_extra(cls, values: Dict) -> Dict:
        extra = values.get("model_kwargs", {})
        all_required_field_names = get_pydantic_field_names(cls)
        values["model_kwargs"] = build_extra_kwargs(
            extra, values, all_required_field_names
        )
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        anthropic_api_key = convert_to_secret_str(
            values.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY") or ""
        )
        values["anthropic_api_key"] = anthropic_api_key
        values["_client"] = anthropic.Client(
            api_key=anthropic_api_key.get_secret_value()
        )
        values["_async_client"] = anthropic.AsyncClient(
            api_key=anthropic_api_key.get_secret_value()
        )
        return values

    def _format_params(
        self,
        *,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Dict,
    ) -> Dict:
        # get system prompt if any
        system, formatted_messages = _format_messages(messages)
        rtn = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "stop_sequences": stop,
            "system": system,
            **self.model_kwargs,
        }
        rtn = {k: v for k, v in rtn.items() if v is not None}

        return rtn

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        params = self._format_params(messages=messages, stop=stop, **kwargs)
        with self._client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                chunk = ChatGenerationChunk(message=AIMessageChunk(content=text))
                if run_manager:
                    run_manager.on_llm_new_token(text, chunk=chunk)
                yield chunk

    def _my_stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        params = self._format_params(messages=messages, stop=stop, **kwargs)
        with self._client.messages.stream(**params) as stream:
            n = 0
            t = ""
            no_stream_out = False
            for text in stream.text_stream:
                if n < SEARCH_FUNCTION_CALL_SIZE - 1 and not no_stream_out:
                    t = t + text
                    n = n + 1
                    continue
                elif n == SEARCH_FUNCTION_CALL_SIZE - 1:
                    n = n + 1
                    t = t + text
                    if "<function_calls>" in t:
                        no_stream_out = True
                        chunk = ChatGenerationChunk(message=AIMessageChunk(content=t))
                        yield chunk
                else:
                    chunk = ChatGenerationChunk(message=AIMessageChunk(content=text))
                    if not no_stream_out:
                        if run_manager:
                            run_manager.on_llm_new_token(text, chunk=chunk)
                    yield chunk

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        params = self._format_params(messages=messages, stop=stop, **kwargs)
        async with self._async_client.messages.stream(**params) as stream:
            async for text in stream.text_stream:
                chunk = ChatGenerationChunk(message=AIMessageChunk(content=text))
                if run_manager:
                    await run_manager.on_llm_new_token(text, chunk=chunk)
                yield chunk

    def _format_output(
        self,
        data: Any,
        **kwargs: Any,
    ) -> ChatResult:
        return ChatResult(
            generations=[
                ChatGeneration(message=AIMessageChunk(content=data.content[0].text))
            ],
            llm_output=data,
        )

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            stream_iter = self._my_stream(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
            generation = ""
            for chunk in stream_iter:
                if generation is None:
                    generation = chunk.message.content
                else:
                    generation += chunk.message.content
            # result = await agenerate_from_stream(stream_iter)
            return self._format_output(generation, **kwargs)
            # return generate_from_stream(stream_iter)
        params = self._format_params(messages=messages, stop=stop, **kwargs)
        data = self._client.messages.create(**params)
        return self._format_output(data, **kwargs)

    async def _astream_my(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        params = self._format_params(messages=messages, stop=stop, **kwargs)
        async with self._async_client.messages.stream(**params) as stream:
            n = 0
            t = ""
            no_stream_out = False
            async for text in stream.text_stream:
                if n < SEARCH_FUNCTION_CALL_SIZE - 1 and not no_stream_out:
                    t = t + text
                    n = n + 1
                    continue
                elif n == SEARCH_FUNCTION_CALL_SIZE - 1:
                    n = n + 1
                    t = t + text
                    if "<function_calls>" in t:
                        no_stream_out = True
                        chunk = ChatGenerationChunk(message=AIMessageChunk(content=t))
                        yield chunk
                else:
                    chunk = ChatGenerationChunk(message=AIMessageChunk(content=text))
                    if not no_stream_out:
                        if run_manager:
                            await run_manager.on_llm_new_token(text, chunk=chunk)
                    yield chunk

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            stream_iter = self._astream_my(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
            generation = ""
            async for chunk in stream_iter:
                if generation is None:
                    generation = chunk.message.content
                else:
                    generation += chunk.message.content
            # result = await agenerate_from_stream(stream_iter)
            return self._format_output(generation, **kwargs)
        params = self._format_params(messages=messages, stop=stop, **kwargs)
        data = await self._async_client.messages.create(**params)
        resutl = self._format_output(data, **kwargs)
        return resutl

    def _format_output_my(self, text: str, **kwargs: Any) -> ChatResult:
        """Format the output of the model, parsing xml as a tool call."""
        tools = kwargs.get("tools", None)

        additional_kwargs: Dict[str, Any] = {}

        if tools:
            # parse out the xml from the text
            try:
                # get everything between <function_calls> and </function_calls>
                start = text.find("<function_calls>")
                end = text.find("</function_calls>") + len("</function_calls>")
                xml_text = text[start:end]

                xml = self._xmllib.fromstring(xml_text)
                additional_kwargs["tool_calls"] = _xml_to_tool_calls(xml, tools)
                text = ""
            except Exception:
                pass

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessageChunk(
                        content=text, additional_kwargs=additional_kwargs
                    )
                )
            ],
            # llm_output=data,
        )


def _xml_to_dict(t: Any) -> Union[str, Dict[str, Any]]:
    # Base case: If the element has no children, return its text or an empty string.
    if len(t) == 0:
        return t.text or ""

    # Recursive case: The element has children. Convert them into a dictionary.
    d: Dict[str, Any] = {}
    for child in t:
        if child.tag not in d:
            d[child.tag] = _xml_to_dict(child)
        else:
            # Handle multiple children with the same tag
            if not isinstance(d[child.tag], list):
                d[child.tag] = [d[child.tag]]  # Convert existing entry into a list
            d[child.tag].append(_xml_to_dict(child))
    return d


def _xml_to_function_call(invoke: Any, tools: List[Dict]) -> Dict[str, Any]:
    name = invoke.find("tool_name").text
    arguments = _xml_to_dict(invoke.find("parameters"))

    # make list elements in arguments actually lists
    filtered_tools = [tool for tool in tools if tool["name"] == name]
    if len(filtered_tools) > 0 and not isinstance(arguments, str):
        tool = filtered_tools[0]
        for key, value in arguments.items():
            if key in tool["parameters"]["properties"]:
                if "type" in tool["parameters"]["properties"][key]:
                    if tool["parameters"]["properties"][key][
                        "type"
                    ] == "array" and not isinstance(value, list):
                        arguments[key] = [value]
                    if (
                        tool["parameters"]["properties"][key]["type"] != "object"
                        and isinstance(value, dict)
                        and len(value.keys()) == 1
                    ):
                        arguments[key] = list(value.values())[0]

    return {
        "function": {
            "name": name,
            "arguments": json.dumps(arguments),
        },
        "type": "function",
    }


def _xml_to_tool_calls(elem: Any, tools: List[Dict]) -> List[Dict[str, Any]]:
    """
    Convert an XML element and its children into a dictionary of dictionaries.
    """
    invokes = elem.findall("invoke")

    return [_xml_to_function_call(invoke, tools) for invoke in invokes]


@deprecated(since="0.1.0", removal="0.2.0", alternative="ChatAnthropic")
class ChatAnthropicMessages(ChatAnthropic):
    pass
