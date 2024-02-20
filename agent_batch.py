from typing import Any, Dict, List, Optional, Sequence, Union
from pathlib import Path
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain.agents import AgentExecutor
from langchain.agents import Tool

# from callback import AgentCallbackHandler
# from langchain.callbacks.manager import AsyncCallbackManager
from langchain_openai import ChatOpenAI
import os
from datetime import datetime
import re
from html import unescape
from openai_assistant_tools import TradingviewWrapper
from langchain.agents import tool
from metaphor_python import Metaphor
import json
import os


from langchain.agents import Tool
from openai_assistant_tools import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
from openai_assistant_tools import MyAPIChain

# from langsmith import Client
from pydantic import BaseModel, Extra, Field
from fastapi.middleware.cors import CORSMiddleware
import openai_assistant_api_docs

import openai_assistant_api_docs
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from datetime import datetime
from langchain_core.output_parsers import StrOutputParser
import asyncio
from langchain_community.tools.convert_to_openai import format_tool_to_openai_tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents import load_tools
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.runnables import ConfigurableField

if getattr(sys, "frozen", False):
    script_location = Path(sys.executable).parent.resolve()
else:
    script_location = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=script_location / ".env")

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


def create_agent_executor() -> AgentExecutor:
    llm_agent = ChatOpenAI(
        temperature=0.7,
        model="gpt-4-turbo-preview",
        verbose=True,
        streaming=True,
    ).configurable_alternatives(  # This gives this field an id
        # When configuring the end runnable, we can then use this id to configure this field
        ConfigurableField(id="llm"),
        default_key="openai_gpt_4_turbo_preview",
        openai_gpt_3_5_turbo_1106=ChatOpenAI(
            model="gpt-3.5-turbo-1106",
            verbose=True,
            streaming=True,
            temperature=0.7,
        ),
    )
    # agent_cb_manager = AsyncCallbackManager([agent_cb_handler])
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        verbose=True,
    )
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("CMC_API_KEY"),
    }
    cmc_last_quote_api = MyAPIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=openai_assistant_api_docs.cmc_quote_lastest_api_doc,
        headers=headers,
        limit_to_domains=["https://pro-api.coinmarketcap.com"],
        verbose=True,
    )
    cmc_trending_latest_api = MyAPIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=openai_assistant_api_docs.cmc_trending_latest_api_doc,
        headers=headers,
        limit_to_domains=["https://pro-api.coinmarketcap.com"],
        verbose=True,
    )
    cmc_trending_gainers_losers_api = MyAPIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=openai_assistant_api_docs.cmc_trending_gainers_losers_api_doc,
        headers=headers,
        limit_to_domains=["https://pro-api.coinmarketcap.com"],
        verbose=True,
    )
    cmc_trending_most_visited_api = MyAPIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=openai_assistant_api_docs.cmc_trending_most_visited_api_doc,
        headers=headers,
        limit_to_domains=["https://pro-api.coinmarketcap.com"],
        verbose=True,
    )
    cmc_metadata_api = MyAPIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=openai_assistant_api_docs.cmc_metadata_api_doc,
        headers=headers,
        limit_to_domains=["https://pro-api.coinmarketcap.com"],
        verbose=True,
    )

    tradingview = TradingviewWrapper(llm=llm)

    @tool
    def search(query: str, search_type: str = None) -> str:
        """Search for a webpage with Google based on the query.
        Set the optional search_type (str) parameter to specify whether to search news (search_type='news') or web pages (search_type=None).
        """
        if search_type == "news":
            newsSearch = GoogleSerperAPIWrapper(type=search_type, tbs="qdr:h")
            return json.dumps(
                [
                    {
                        "title": r["title"],
                        "link": r["link"],
                        "snippet": r["snippet"],
                        "imageUrl": r["imageUrl"],
                    }
                    for r in newsSearch.results(query=query)["news"]
                ]
            )
        else:
            searchWebpage = GoogleSerperAPIWrapper()
            return json.dumps(
                [
                    {
                        "title": r["title"],
                        "link": r["link"],
                        "snippet": r["snippet"],
                    }
                    for r in searchWebpage.results(query=query)["organic"]
                ]
            )

    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile("<.*?>")
        text = re.sub(clean, "", text)  # Remove HTML tags
        text = unescape(text)  # Unescape HTML entities
        return text

    from pyppeteer import launch

    async def fetch_page(url):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        html_content = await page.content()
        await browser.close()
        return html_content

    @tool
    async def get_contents(links: List[str]):
        """Get the contents of a webpage.
        The links passed in should be a list of links returned from `search`.
        """
        req_tasks = []
        results = []
        for url in links:
            req_tasks.append(fetch_page(url=url))
            results.append(
                {
                    "url": url,
                }
            )
        contents = await asyncio.gather(*req_tasks)
        extract_task = []
        for _content in contents:
            no_html = remove_html_tags(_content)
            prompt = ChatPromptTemplate.from_template(
                """I have a piece of text that I need you to help summarize, but please ensure that the summary does not exceed 100 words. Here is the text that needs to be summarized: {input}."""
            )
            model = ChatOpenAI(model="gpt-3.5-turbo-1106", verbose=True)
            output_parser = StrOutputParser()
            chain = prompt | model | output_parser
            task = chain.with_config({"verbose": True}).ainvoke({"input": no_html})
            extract_task.append(task)
        _extracts = await asyncio.gather(*extract_task)
        for i in range(len(results)):
            results[i]["extract"] = _extracts[i]
        return json.dumps(results) if len(results) > 0 else f"There is no any result"

    # from langchain_community.tools.arxiv.tool import ArxivQueryRun
    from arxiv_wrapper import ArxivAPIWrapper

    # arxiv = ArxivQueryRun()

    @tool
    def arxiv_search(query: str):
        """A wrapper around Arxiv.org
        Useful for when you need to answer questions about Physics, Mathematics,
        Computer Science, Quantitative Biology, Quantitative Finance, Statistics,
        Electrical Engineering, and Economics
        from scientific articles on arxiv.org.
        Input should be a search query."""
        api_wrapper = ArxivAPIWrapper(doc_content_chars_max=10000)
        return api_wrapper.run(query=query)

    @tool
    def arxiv_load(entry_id: str):
        """Useful for when your need to know the content of some paper on Arxiv.org.
        Input should be the entry_id return from `arxiv_search`."""
        api_wrapper = ArxivAPIWrapper(doc_content_chars_max=10000)
        return api_wrapper.load(query=entry_id)

    import requests
    from bs4 import BeautifulSoup

    @tool
    def getHTMLFromURL(url: str) -> str:
        """useful when you need get the HTML of URL. The input to this should be URL."""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find('article', id='content')

    @tool
    async def getHTMLFromURLs(urls: list[str]) -> str:
        """useful when you need get the HTML of URLs. The input to this should be URL list."""
        req_tasks = []
        for url in urls:
            req_tasks.append(fetch_page(url=url))
        contents = await asyncio.gather(*req_tasks)
        result = ""
        for c in contents:
            soup = BeautifulSoup(c, "html.parser")
            result += "\n" + remove_html_tags(soup.prettify())
        return result

    tools = [
        search,
        getHTMLFromURL,
        getHTMLFromURLs,
        Tool(
            name="CryptocurrencyLatestQuote",
            func=cmc_last_quote_api.run,
            description="""useful when you need get a cryptocurrency's latest quote. The input to this should be a single cryptocurrency's symbol.""",
            coroutine=cmc_last_quote_api.arun,
        ),
        Tool(
            name="TrendingLatest",
            func=cmc_trending_latest_api.run,
            description="""useful when you need get a list of all trending cryptocurrency market data, determined and sorted by CoinMarketCap search volume. The input to this should be a complete question in English, and the question must have a ranking requirement, and the ranking cannot exceed 20.""",
            coroutine=cmc_trending_latest_api.arun,
        ),
        Tool(
            name="TrendingGainersAndLosers",
            func=cmc_trending_gainers_losers_api.run,
            description="""useful when you need get a list of all trending cryptocurrencies, determined and sorted by the largest price gains or losses. The input to this should be a complete question in English, and the question must have a ranking requirement, and the ranking cannot exceed 20.""",
            coroutine=cmc_trending_gainers_losers_api.arun,
        ),
        Tool(
            name="TrendingMostVisited",
            func=cmc_trending_most_visited_api.run,
            description="""useful when you need get a list of all trending cryptocurrency market data, determined and sorted by traffic to coin detail pages. The input to this should be a complete question in English, and the question must have a ranking requirement, and the ranking cannot exceed 20.""",
            coroutine=cmc_trending_most_visited_api.arun,
        ),
        Tool(
            name="MetaDataOfCryptocurrency",
            func=cmc_metadata_api.run,
            description="""useful when you need get all static metadata available for one or more cryptocurrencies. This information includes details like logo, description, official website URL, social links, and links to a cryptocurrency's technical documentation. The input to this should be a complete question in English.""",
            coroutine=cmc_metadata_api.arun,
        ),
        Tool(
            name="BuyOrSellSignal",
            func=tradingview.buySellSignal,
            description="""Useful when you need to know buy and sell signals for a cryptocurrency. The input to this should be a cryptocurrency's symbol.""",
            coroutine=tradingview.abuySellSignal,
        ),
        arxiv_search,
        arxiv_load,
    ]
    date = datetime.now().strftime("%b %d %Y")

    system_message = (
        f"Today is {date}.\n\n"
        + """Act as a useful assistant.

Don’t state disclaimers about your knowledge cutoff.

Don’t state you are an AI language model.
"""
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(template=system_message),
            # MessagesPlaceholder(variable_name="chat_history"),
            # SystemMessagePromptTemplate.from_template(
            #     "If using the search tool, prefix the string parameter with [S]."
            # ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    llm_with_tools = llm_agent.bind(
        tools=[format_tool_to_openai_tool(tool) for tool in tools]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            # "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        # | prompt_trimmer # See comment above.
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    executor = AgentExecutor(
        agent=agent.with_config({"run_name": "Eddie_Assistant"}),
        tools=tools,
        verbose=True,
    )
    return executor


agent_executor = create_agent_executor()
