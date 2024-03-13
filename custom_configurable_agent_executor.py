from typing import Any, AsyncIterator, Dict, List, Optional, Sequence, cast
from typing_extensions import Literal

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.runnables import (
    ConfigurableFieldSpec,
    Runnable,
    RunnableConfig,
)
from langchain_core.runnables.schema import EventData, StreamEvent


class CustomAgentExecutor(Runnable):
    """A custom runnable that will be used by the agent executor."""

    def __init__(self, **kwargs):
        """Initialize the runnable."""
        super().__init__(**kwargs)
        self.agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_functions(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

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
            tools=tools,
        ).with_config({"run_name": "executor"})

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
