from typing import Any, Dict, List, Literal, Optional, Sequence
from langchain_core.runnables.schema import StreamEvent
from typing import AsyncIterator, cast
from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Input, Output
from langchain_core.runnables import (
    ConfigurableFieldSpec,
    RunnableConfig,
)
from langchain.agents import AgentExecutor
from langchain_core.tools import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser


class CustomAgentExecutor(Runnable):
    """A custom runnable that will be used by the agent executor."""

    def __init__(self, agent: Runnable, tools: List[BaseTool], **kwargs):
        """Initialize the runnable."""
        super().__init__(**kwargs)
        self.agent = agent
        self.tools = tools

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        """Will not be used."""
        raise NotImplementedError()

    @property
    def config_specs(self) -> List[ConfigurableFieldSpec]:
        return self.agent.config_specs

    async def astream_events(
        self,
        input: Any,
        config: Optional[RunnableConfig] = None,
        *,
        version: Literal["v1"],
        include_names: Optional[Sequence[str]] = None,
        include_types: Optional[Sequence[str]] = None,
        include_tags: Optional[Sequence[str]] = None,
        exclude_names: Optional[Sequence[str]] = None,
        exclude_types: Optional[Sequence[str]] = None,
        exclude_tags: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        configurable = cast(Dict[str, Any], config.pop("configurable", {}))
        if configurable:
            configured_agent = self.agent.with_config(
                {
                    "configurable": configurable,
                }
            )
        else:
            configured_agent = self.agent

        executor = AgentExecutor(
            agent=configured_agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        ).with_config({"run_name": "Eddie's Assistant Agent"})

        async for output in executor.astream_events(
            input,
            config=config,
            version=version,
            include_names=include_names,
            include_tags=include_tags,
            include_types=include_types,
            exclude_names=exclude_names,
            exclude_tags=exclude_tags,
            exclude_types=exclude_types,
            **kwargs,
        ):
            yield output


class CustomToolCallingAgentExecutor(Runnable):
    """A custom runnable that will be used by the agent executor."""

    def __init__(
        self,
        llm: BaseChatModel,
        prompts: ChatPromptTemplate,
        tools: List[BaseTool],
        **kwargs,
    ):
        """Initialize the runnable."""
        super().__init__(**kwargs)
        self.llm = llm
        self.tools = tools
        self.prompts = prompts

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        """Will not be used."""
        raise NotImplementedError()

    @property
    def config_specs(self) -> List[ConfigurableFieldSpec]:
        return self.llm.config_specs

    async def astream_events(
        self,
        input: Any,
        config: Optional[RunnableConfig] = None,
        *,
        version: Literal["v1"],
        include_names: Optional[Sequence[str]] = None,
        include_types: Optional[Sequence[str]] = None,
        include_tags: Optional[Sequence[str]] = None,
        exclude_names: Optional[Sequence[str]] = None,
        exclude_types: Optional[Sequence[str]] = None,
        exclude_tags: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        configurable = cast(Dict[str, Any], config.pop("configurable", {}))

        if configurable:
            configured_llm = self.llm.with_config(
                {
                    "configurable": configurable,
                }
            )
        else:
            configured_llm = self.llm
        llm_agent = configured_llm.bind_tools(tools=self.tools)
        agent = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_to_tool_messages(
                    x["intermediate_steps"]
                )
            )
            | self.prompts
            | llm_agent
            | ToolsAgentOutputParser()
        )

        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        ).with_config({"run_name": "Eddie's Assistant Agent"})

        async for output in executor.astream_events(
            input,
            config=config,
            version=version,
            include_names=include_names,
            include_tags=include_tags,
            include_types=include_types,
            exclude_names=exclude_names,
            exclude_tags=exclude_tags,
            exclude_types=exclude_types,
            **kwargs,
        ):
            yield output
