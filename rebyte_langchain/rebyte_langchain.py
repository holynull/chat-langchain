from __future__ import annotations

import logging
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.chat_models.base import BaseChatModel
from langchain.pydantic_v1 import Field, root_validator
from langchain.schema import ChatGeneration, ChatResult
from langchain.schema.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    BaseMessageChunk,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
)
from langchain.schema.output import ChatGenerationChunk
from langchain.utils import get_from_dict_or_env
from langchain_core.utils.function_calling import convert_to_openai_tool

logger = logging.getLogger(__name__)
logger_formatter = "%(asctime)s - rebyte-langchain-SDK - %(funcName)s - %(filename)s - %(levelname)s - %(message)s"

logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
ch_format = logging.Formatter(logger_formatter)
console_handler.setFormatter(ch_format)
logger.addHandler(console_handler)


def _convert_resp_to_message_chunk(text: str) -> BaseMessageChunk:
    return AIMessageChunk(
        content=text,
        role="assistant",
    )


def convert_message_to_dict(message: BaseMessage) -> dict:
    message_dict: Dict[str, Any]
    if isinstance(message, ChatMessage):
        message_dict = {"role": message.role, "content": message.content}
    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        message_dict = {"role": "assistant", "content": message.content}
        if "function_call" in message.additional_kwargs:
            message_dict["functions"] = message.additional_kwargs["function_call"]
            # If function call only, content is None not empty string
            if message_dict["content"] == "":
                message_dict["content"] = None
    elif isinstance(message, FunctionMessage):
        message_dict = {
            "role": "function",
            "content": message.content,
            "name": message.name,
        }
    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}
    else:
        raise TypeError(f"Got unknown type {message}")

    if "parts" in message.additional_kwargs:
        message_dict["parts"] = message.additional_kwargs["parts"]

    return message_dict


class RebyteEndpoint(BaseChatModel):

    model_kwargs: Dict[str, Any] = Field(default_factory=dict)

    rebyte_api_key: Optional[str] = None

    client: Any

    agent_id: Optional[str] = None
    """The callable id of the ReByte agent"""
    project_id: Optional[str] = None
    """The project id of the ReByte agent"""
    session_id: Optional[str] = None
    """The session id of the ReByte agent. You must provide a session id to enable stateful actions, such as threads (aka, memory), in the agent."""

    blocking: Optional[bool] = True
    """Whether to use blocking or not."""
    version: Optional[Union[str, int]] = "latest"
    """The version of the ReByte agent"""

    streaming: Optional[bool] = False
    """Whether to stream the results or not."""

    request_timeout: Optional[int] = 60
    """request timeout for chat http requests"""

    endpoint: Optional[str] = None
    """Endpoint of the ReByte LLM, required if custom model used."""

    @root_validator()
    def validate_enviroment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(
            values,
            "rebyte_api_key",
            "REBYTE_API_KEY",
        )
        values["endpoint"] = "https://rebyte.ai"

        try:
            import rebyte

            values["client"] = rebyte.RebyteAPIRequestor(
                key=values["api_key"], api_base=values["endpoint"]
            )
        except ImportError:
            raise ValueError(
                "rebyte package not found, please install it with "
                "`pip install rebyte`"
            )
        return values

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            **{
                "endpoint": self.endpoint,
                "agent": self.agent_id,
                "project": self.project_id,
            },
            **super()._identifying_params,
        }

    @property
    def _llm_type(self) -> str:
        """Return type of chat_model."""
        return "rebyte"

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        normal_params = {
            "stream": self.streaming,
            "request_timeout": self.request_timeout,
        }

        return {**normal_params, **self.model_kwargs}

    def _convert_callable_params(
        self,
        messages: List[BaseMessage],
        **kwargs: Any,
    ) -> Dict:
        return {
            "inputs": [
                {
                    "messages": [convert_message_to_dict(m) for m in messages],
                }
            ],
            "version": self.version,
            "session_id": self.session_id,
            "config": {},
            "stream": self.streaming,
            "blocking": self.blocking,
            "block_filter": None,
        }

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            completion = ""
            for chunk in self._stream(messages, stop, run_manager, **kwargs):
                completion += chunk.text
            lc_msg = AIMessage(content=completion, additional_kwargs={})
            gen = ChatGeneration(
                message=lc_msg,
                generation_info=dict(finish_reason="stop"),
            )
            return ChatResult(
                generations=[gen],
                llm_output={"token_usage": {}},
            )
        params = self._convert_callable_params(messages, **kwargs)
        response_payload = self._call_callable(data=params).data
        lc_msg = AIMessage(
            content=self._extract_content_from_response(response_payload),
            additional_kwargs={},
        )
        gen = ChatGeneration(
            message=lc_msg,
            generation_info=dict(finish_reason="stop"),
        )
        token_usage = response_payload.get("usage", {})
        llm_output = {"token_usage": token_usage}
        return ChatResult(generations=[gen], llm_output=llm_output)

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            completion = ""
            token_usage = {}
            async for chunk in self._astream(messages, stop, run_manager, **kwargs):
                completion += chunk.text

            lc_msg = AIMessage(content=completion, additional_kwargs={})
            gen = ChatGeneration(
                message=lc_msg,
                generation_info=dict(finish_reason="stop"),
            )
            return ChatResult(
                generations=[gen],
                llm_output={"token_usage": {}},
            )
        params = self._convert_callable_params(messages, **kwargs)
        response_payload = await self._acall_callable(params).data
        lc_msg = AIMessage(
            content=self._extract_content_from_response(response_payload),
            additional_kwargs={},
        )
        generations = []
        gen = ChatGeneration(
            message=lc_msg,
            generation_info=dict(finish_reason="stop"),
        )
        generations.append(gen)
        token_usage = response_payload.get("usage", {})
        llm_output = {"token_usage": token_usage}
        return ChatResult(generations=generations, llm_output=llm_output)

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        params = self._convert_callable_params(messages, **kwargs)
        for res in self._call_callable(params):
            stream_text = res.get_stream_chunk()
            if res and stream_text:
                chunk = ChatGenerationChunk(
                    text=stream_text,
                    message=_convert_resp_to_message_chunk(stream_text),
                )
                yield chunk
                if run_manager:
                    run_manager.on_llm_new_token(chunk.text, chunk=chunk)

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        params = self._convert_callable_params(messages, **kwargs)
        async for res in await self._acall_callable(params):
            stream_text = res.get_stream_chunk()
            if stream_text:
                chunk = ChatGenerationChunk(
                    text=stream_text,
                    message=_convert_resp_to_message_chunk(stream_text),
                )
                yield chunk
                if run_manager:
                    await run_manager.on_llm_new_token(chunk.text, chunk=chunk)

    def _call_callable(self, data: Dict):
        path = f"/api/sdk/p/{self.project_id}/a/{self.agent_id}/r"
        try:
            res, _, _ = self.client.request(
                method="POST", stream=self.streaming or False, url=path, params=data
            )
        except Exception as e:
            logger.error(str(e))
            raise e

        return res

    async def _acall_callable(self, data: Dict):
        path = f"/api/sdk/p/{self.project_id}/a/{self.agent_id}/r"
        try:
            res, _, _ = await self.client.arequest(
                method="POST", stream=self.streaming or False, url=path, params=data
            )
        except Exception as e:
            logger.error(str(e))
            raise e

        return res

    def _extract_content_from_response(self, response: Dict) -> str:
        run = response.get("run")
        if run:
            results = run.get("results")
            if results:
                result = results[0][0]
                if result.get("error"):
                    raise result.get("error")
                if result.get("value") is None:
                    raise "No value found"
                return (
                    result["value"]["content"] if "content" in result["value"] else ""
                )
