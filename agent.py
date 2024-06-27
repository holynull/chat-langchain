from pathlib import Path
import sys
from fastapi import FastAPI
from dotenv import load_dotenv

from my_langchain_anthropic.experimental import ChatAnthropicTools
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatPerplexity
from langchain_mistralai import ChatMistralAI
from langchain_cohere import ChatCohere

# from callback import AgentCallbackHandler
# from langchain.callbacks.manager import AsyncCallbackManager
from datetime import datetime


# from langsmith import Client
from fastapi.middleware.cors import CORSMiddleware

from langchain.agents import AgentExecutor
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from datetime import datetime
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from anthropic_tools import (
    AnthropicToolsAgentOutputParser,
    format_to_anthropic_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

# from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain_core.runnables import ConfigurableField
from langchain_core.runnables import Runnable


from langchain import hub
from tools_basic import tools
from eddie_tools import getHTMLOfURL

if getattr(sys, "frozen", False):
    script_location = Path(sys.executable).parent.resolve()
else:
    script_location = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=script_location / ".env")

from langsmith import Client

langsmith_client = Client()

# client = Client()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def create_agent_executor(llm_agent: Runnable) -> AgentExecutor:

    date = datetime.now().strftime("%b %d %Y")
    # Please evaluate whether to answer the question by searching the web or searching the news, or answering the question in another way.
    # Don't say you can't directly access the content of external web pages. You can access specific web content on the Internet through the `answerQuestionFromLinks` tool.

    system_message = (
        f"Today is {date}.\n\n"
        + """As a useful assistant.
"""
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            # SystemMessagePromptTemplate.from_template(
            #     "If using the search tool, prefix the string parameter with [S]."
            # ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    from langchain.tools.render import render_text_description
    from langchain_core.runnables import RunnablePassthrough
    from langchain.agents.format_scratchpad import format_log_to_str
    from langchain.agents.output_parsers import ReActSingleInputOutputParser

    react_prompt = hub.pull("hwchase17/react-chat")
    react_prompt = react_prompt.partial(
        tools=render_text_description(list(tools)),
        tool_names=", ".join([t.name for t in tools]),
    )
    openai_agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        # | prompt_trimmer # See comment above.
        | llm_agent.bind(tools=[convert_to_openai_tool(tool) for tool in tools])
        | OpenAIToolsAgentOutputParser()
    )
    anthropic_agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        # | prompt_trimmer # See comment above.
        | llm_agent.bind(tools=[convert_to_openai_function(tool) for tool in tools])
        | AnthropicToolsAgentOutputParser()
    )
    react_agent = (
        # {
        #     "input": lambda x: x["input"],
        #     "agent_scratchpad": lambda x: format_log_to_str(
        #         x["intermediate_steps"]
        #     ),
        #     "chat_history": lambda x: x["chat_history"],
        # }
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
        )
        | react_prompt
        | llm_agent.bind(stop=["\nObservation"])
        | ReActSingleInputOutputParser()
    )
    # agent = anthropic_agent.configurable_alternatives(
    #     which=ConfigurableField("llm"),
    #     default_key="anthropic_claude_3_opus",
    #     openai_gpt_4_turbo_preview=openai_agent,
    #     openai_gpt_3_5_turbo_1106=openai_agent,
    #     pplx_sonar_medium_chat=react_agent,
    #     mistral_large=react_agent,
    #     command_r_plus=react_agent,
    # )
    # llm_with_tools = llm_agent.bind_tools(tools=tools)

    from custom_agent_excutor import CustomAgentExecutor, CustomToolCallingAgentExecutor

    executor = CustomToolCallingAgentExecutor(
        llm=llm_agent, prompts=prompt, tools=tools
    )
    return executor


llm_agent = ChatAnthropic(
    model="claude-3-opus-20240229",
    # max_tokens=,
    temperature=0.9,
    # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
    streaming=True,
    verbose=True,
).configurable_alternatives(  # This gives this field an id
    # When configuring the end runnable, we can then use this id to configure this field
    ConfigurableField(id="llm"),
    # default_key="openai_gpt_4_turbo_preview",
    default_key="anthropic_claude_3_opus",
    openai_gpt_3_5_turbo_1106=ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        verbose=True,
        streaming=True,
        temperature=0.9,
    ),
    openai_gpt_4_turbo_preview=ChatOpenAI(
        temperature=0.9,
        model="gpt-4-turbo-preview",
        verbose=True,
        streaming=True,
    ),
	openai_gpt_4o=ChatOpenAI(
        temperature=0.9,
        model="gpt-4o",
        verbose=True,
        streaming=True,
    ),
    pplx_sonar_medium_chat=ChatPerplexity(
        model="sonar-medium-chat", temperature=0.9, verbose=True, streaming=True
    ),
    mistral_large=ChatMistralAI(
        model="mistral-large-latest", temperature=0.1, verbose=True, streaming=True
    ),
    command_r_plus=ChatCohere(
        model="command-r-plus", temperature=0.9, verbose=True, streaming=True
    ),
)

agent_executor = create_agent_executor(llm_agent=llm_agent)
