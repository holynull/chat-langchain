import requests
from langchain_community.agent_toolkits import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain_openai import ChatOpenAI
from langchain.agents import Agent
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_community.tools.convert_to_openai import format_tool_to_openai_tool
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from my_langchain_anthropic.experimental import ChatAnthropicTools
from langchain_core.runnables import ConfigurableField
from anthropic_tools import (
    AnthropicToolsAgentOutputParser,
    format_to_anthropic_tool_messages,
)
from langchain_core.utils.function_calling import convert_to_openai_function


class DefiLLamaWrapTVLofPtotocols:
    def __init__(self):
        self.url = "https://api.llama.fi/protocols"
        self.headers = {"accept": "*/*"}
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data:
                json_data[d["name"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

    def create_agent(self) -> Agent:
        llm_agent = ChatAnthropicTools(
            model="claude-3-opus-20240229",
            # max_tokens=,
            temperature=0.7,
            # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
            streaming=True,
            verbose=True,
        ).configurable_alternatives(  # This gives this field an id
            # When configuring the end runnable, we can then use this id to configure this field
            ConfigurableField(id="llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_3_5_turbo_0125=ChatOpenAI(
                model="gpt-3.5-turbo-0125",
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
        )
        system_message = """You are a very useful assistant. 

        Please first use json_spec_list_keys(data) to find the relevant keys, and then call json_spec_get_value with the most relevant key.

        For example, when json_spec_get_value(data["key1"]) returns a KeyError, please call json_spec_list_keys(data) again to find a key2 related to "key1", and then call json_spec_get_value(data["key2"]) again.

        In the JSON file, key `chains` is an array of string. It means the project has tvl on those chains.

        And the key 'chainTvls' is a obj, it means the tvl on chains.

        `change_1h` represents the change of tvl within 1 hour.
        `change_1d` represents the change of tvl within 1 day. 
        `change_7d` represents the change of tvl within 7 days.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
            openai_gpt_3_5_turbo_0125=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            # | prompt_trimmer # See comment above.
            | llm_agent.bind(
                tools=[convert_to_openai_function(tool) for tool in self.tools]
            )
            | AnthropicToolsAgentOutputParser()
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
            openai_gpt_3_5_turbo_0125=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
        )
        return agent

    def fetch(self):
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data:
                json_data[d["name"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)


class DefiLLamaWrapCirculatingVolumeOfStablecoins:
    def __init__(self):
        self.url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
        self.headers = {"accept": "*/*"}
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["peggedAssets"]:
                json_data[d["name"] + "(" + d["symbol"] + ")"] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

    def create_agent(self) -> Agent:
        llm_agent = ChatAnthropicTools(
            model="claude-3-opus-20240229",
            # max_tokens=,
            temperature=0.7,
            # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
            streaming=True,
            verbose=True,
        ).configurable_alternatives(  # This gives this field an id
            # When configuring the end runnable, we can then use this id to configure this field
            ConfigurableField(id="llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_3_5_turbo_0125=ChatOpenAI(
                model="gpt-3.5-turbo-0125",
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
        )
        system_message = """You are a very useful assistant. 

        Please first use json_spec_list_keys(data) to find the relevant keys, and then call json_spec_get_value with the most relevant key.

        For example, when json_spec_get_value(data["key1"]) returns a KeyError, please call json_spec_list_keys(data) again to find a key2 related to "key1", and then call json_spec_get_value(data["key2"]) again.

        In the JSON file, `chainCirculating` means the circulating volume of chains.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
            openai_gpt_3_5_turbo_0125=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            # | prompt_trimmer # See comment above.
            | llm_agent.bind(
                tools=[convert_to_openai_function(tool) for tool in self.tools]
            )
            | AnthropicToolsAgentOutputParser()
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
            openai_gpt_3_5_turbo_0125=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
        )
        return agent

    def fetch(self):
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["peggedAssets"]:
                json_data[d["name"] + "(" + d["symbol"] + ")"] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)


class DefiLLamaWrapTotalCirculatingVolumeOfStablecoins:
    def __init__(self):
        self.url = "https://stablecoins.llama.fi/stablecoinchains"
        self.headers = {"accept": "*/*"}
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data:
                json_data[
                    d["name"]
                    + "("
                    + (d["tokenSymbol"] if d["tokenSymbol"] else "")
                    + ")"
                ] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

    def create_agent(self) -> Agent:
        llm_agent = ChatAnthropicTools(
            model="claude-3-opus-20240229",
            # max_tokens=,
            temperature=0.7,
            # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
            streaming=True,
            verbose=True,
        ).configurable_alternatives(  # This gives this field an id
            # When configuring the end runnable, we can then use this id to configure this field
            ConfigurableField(id="llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_3_5_turbo_0125=ChatOpenAI(
                model="gpt-3.5-turbo-0125",
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
        )
        system_message = """You are a very useful assistant. 

        Please first use json_spec_list_keys(data) to find the relevant keys, and then call json_spec_get_value with the most relevant key.

        For example, when json_spec_get_value(data["key1"]) returns a KeyError, please call json_spec_list_keys(data) again to find a key2 related to "key1", and then call json_spec_get_value(data["key2"]) again.

        In the JSON file, `totalCirculatingUSD` means the USD value of the fiat currency pegged to the chain.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
            openai_gpt_3_5_turbo_0125=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            # | prompt_trimmer # See comment above.
            | llm_agent.bind(
                tools=[convert_to_openai_function(tool) for tool in self.tools]
            )
            | AnthropicToolsAgentOutputParser()
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
            openai_gpt_3_5_turbo_0125=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
        )
        return agent

    def fetch(self):
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data:
                json_data[
                    d["name"]
                    + "("
                    + (d["tokenSymbol"] if d["tokenSymbol"] else "")
                    + ")"
                ] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)


class DefiLLamaWrapYeildsAPYOfPools:
    def __init__(self):
        self.url = "https://yields.llama.fi/pools"
        self.headers = {"accept": "*/*"}
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["data"]:
                json_data[d["project"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

    def create_agent(self) -> Agent:
        llm_agent = ChatAnthropicTools(
            model="claude-3-opus-20240229",
            # max_tokens=,
            temperature=0.7,
            # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
            streaming=True,
            verbose=True,
        ).configurable_alternatives(  # This gives this field an id
            # When configuring the end runnable, we can then use this id to configure this field
            ConfigurableField(id="llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_3_5_turbo_0125=ChatOpenAI(
                model="gpt-3.5-turbo-0125",
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
        )
        system_message = """You are a very useful assistant. 

        Please first use json_spec_list_keys(data) to find the relevant keys, and then call json_spec_get_value with the most relevant key.

        For example, when json_spec_get_value(data["key1"]) returns a KeyError, please call json_spec_list_keys(data) again to find a key2 related to "key1", and then call json_spec_get_value(data["key2"]) again.

        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
            openai_gpt_3_5_turbo_0125=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            # | prompt_trimmer # See comment above.
            | llm_agent.bind(
                tools=[convert_to_openai_function(tool) for tool in self.tools]
            )
            | AnthropicToolsAgentOutputParser()
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
            openai_gpt_3_5_turbo_0125=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
        )
        return agent

    def fetch(self):
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["data"]:
                json_data[d["project"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

class DefiLLamaWrapInfoOfBridges:
    def __init__(self):
        self.url = "https://bridges.llama.fi/bridges?includeChains=true"
        self.headers = {"accept": "*/*"}
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["bridges"]:
                json_data[d["name"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

    def create_agent(self) -> Agent:
        llm_agent = ChatAnthropicTools(
            model="claude-3-opus-20240229",
            # max_tokens=,
            temperature=0.7,
            # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
            streaming=True,
            verbose=True,
        ).configurable_alternatives(  # This gives this field an id
            # When configuring the end runnable, we can then use this id to configure this field
            ConfigurableField(id="llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_3_5_turbo_0125=ChatOpenAI(
                model="gpt-3.5-turbo-0125",
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
        )
        system_message = """You are a very useful assistant. 

        Please first use json_spec_list_keys(data) to find the relevant keys, and then call json_spec_get_value with the most relevant key.

        For example, when json_spec_get_value(data["key1"]) returns a KeyError, please call json_spec_list_keys(data) again to find a key2 related to "key1", and then call json_spec_get_value(data["key2"]) again.

        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
            openai_gpt_3_5_turbo_0125=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            # | prompt_trimmer # See comment above.
            | llm_agent.bind(
                tools=[convert_to_openai_function(tool) for tool in self.tools]
            )
            | AnthropicToolsAgentOutputParser()
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
            openai_gpt_3_5_turbo_0125=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
        )
        return agent

    def fetch(self):
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["bridges"]:
                json_data[d["name"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

class DefiLLamaWrapVolumeOfDex:
    def __init__(self):
        self.url = "https://api.llama.fi/overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyVolume"
        self.headers = {"accept": "*/*"}
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["protocols"]:
                json_data[d["name"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)

    def create_agent(self) -> Agent:
        llm_agent = ChatAnthropicTools(
            model="claude-3-opus-20240229",
            # max_tokens=,
            temperature=0.7,
            # anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "not_provided"),
            streaming=True,
            verbose=True,
        ).configurable_alternatives(  # This gives this field an id
            # When configuring the end runnable, we can then use this id to configure this field
            ConfigurableField(id="llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_3_5_turbo_0125=ChatOpenAI(
                model="gpt-3.5-turbo-0125",
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
        )
        system_message = """You are a very useful assistant. 

        Please first use json_spec_list_keys(data) to find the relevant keys, and then call json_spec_get_value with the most relevant key.

        For example, when json_spec_get_value(data["key1"]) returns a KeyError, please call json_spec_list_keys(data) again to find a key2 related to "key1", and then call json_spec_get_value(data["key2"]) again.

        In the JSON file, as follow:
        
        `change_1m` represents the change of dex volume within 1 month.
        `change_1d` represents the change of dex volume within 1 day. 
        `change_7d` represents the change of dex volume within 7 days.
		`change_7dover7d` represents the change of dex volume within 7 days over 7 days.
        `change_30dover30d` represents the change of dex volume within 30 days over 30 days.
		`total24h` represents the total dex volume in 24 hours.
        `total48hto24h` represents the total dex volume in 24 hours over 24 hours.
		`total7d` represents the total dex volume in 7 days.
		`total30d` represents the total dex volume in 30 days.
		`total14dto7d` represents the total dex volume in 7 days over 7 days.
		`total60dto30d` represents the total dex volume in 30 days over 30 days.
		`total1y` represents the total dex volume in 1 year.
		`average1y` represents the average dex volume every year.
		`totalAllTime` represents the total dex volume currently.
        
        ``

        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
            openai_gpt_3_5_turbo_0125=ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(template=system_message),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            ),
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_anthropic_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            # | prompt_trimmer # See comment above.
            | llm_agent.bind(
                tools=[convert_to_openai_function(tool) for tool in self.tools]
            )
            | AnthropicToolsAgentOutputParser()
        ).configurable_alternatives(
            which=ConfigurableField("llm"),
            default_key="anthropic_claude_3_opus",
            openai_gpt_4_turbo_preview=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
            openai_gpt_3_5_turbo_0125=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                # | prompt_trimmer # See comment above.
                | llm_agent.bind(
                    tools=[format_tool_to_openai_tool(tool) for tool in self.tools]
                )
                | OpenAIToolsAgentOutputParser()
            ),
        )
        return agent

    def fetch(self):
        response = requests.get(self.url, headers=self.headers)

        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            json_data = {}
            for d in data["protocols"]:
                json_data[d["name"]] = d
            json_spec = JsonSpec(dict_=json_data, max_value_length=4000)
            json_toolkit = JsonToolkit(spec=json_spec)
            self.tools = json_toolkit.get_tools()
        else:
            raise Exception("请求失败，状态码：", response.status_code)