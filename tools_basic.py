from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
from langchain.agents import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from openai_assistant_tools import GoogleSerperAPIWrapper
from openai_assistant_tools import MyAPIChain
import openai_assistant_api_docs
import json
from openai_assistant_tools import TradingviewWrapper
from html import unescape
from typing import List
import asyncio
import os
from langchain.agents import Tool


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


@tool
def getTokenMetadata(symbol: str) -> str:
    """
    Useful when you need get the metadata of a token.
    """
    url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?symbol={symbol}"
    response = requests.get(url, headers=headers)
    return json.dumps(response.json())


tradingview = TradingviewWrapper(llm=llm)


@tool
def googleSerperSearch(query: str, search_type: str = None) -> str:
    """Search for a webpage with Google based on the query.
    Set the optional search_type (str) parameter to specify whether to search news (search_type='news') or web pages (search_type=None).
    """
    if search_type == "news":
        newsSearch = GoogleSerperAPIWrapper(type=search_type, tbs="qdr:h")
        return json.dumps(
            [
                {
                    "title": r["title"],
                    "link": r["link"] if "link" in r else "",
                    "snippet": r["snippet"],
                    "imageUrl": r["imageUrl"] if "imageUrl" in r else "",
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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@tool
def getHTMLFromURL(url: str) -> str:
    """useful when you need get the HTML of URL. The input to this should be URL."""
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, "html.parser")
    # return soup.prettify()
    driver_path = "chromedriver-mac-x64/chromedriver"
    service = Service(executable_path=driver_path)
    # 创建ChromeOptions对象
    chrome_options = Options()
    # 添加无头模式参数
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # 获取网页内容
    browser.get(url=url)
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    # 找到除了<p>, <img>, <a>以外的所有标签，并删除
    for tag in soup.find_all(True):
        if tag.name in [
            "link",
            "script",
            "style",
            "button",
            "input",
            "meta",
            "iframe",
        ]:
            tag.decompose()
        if tag.attrs is not None and isinstance(tag.attrs, dict):
            tag.attrs = {
                key: value for key, value in tag.attrs.items() if key != "class"
            }

    # 可选：清理空白行
    clean_html = re.sub(r"(?m)^[\t ]+$", "", soup.prettify())
    browser.quit()
    return clean_html


@tool
def getContentFromURL(url: str, tag: str, class_: str) -> str:
    """Useful when you need to get the text content of the html tag in the URL page.
    The parameter `url` is the URL link of the page you need to read.
    The parameters `tag` and `class_` represent extracting the text content of `tag` whose classes attribute is equal to `class_`.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    html = soup.find(tag, class_=class_)
    return remove_html_tags(str(html))


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


from defillama_wrapper import (
    DefiLLamaWrapTVLofPtotocols,
    DefiLLamaWrapCirculatingVolumeOfStablecoins,
    DefiLLamaWrapTotalCirculatingVolumeOfStablecoins,
    DefiLLamaWrapYeildsAPYOfPools,
)

# tvlPotocols = DefiLLamaWrapTVLofPtotocols()
# cvOfSc = DefiLLamaWrapCirculatingVolumeOfStablecoins()
# tcvOfSc = DefiLLamaWrapTotalCirculatingVolumeOfStablecoins()
# apyOfPools = DefiLLamaWrapYeildsAPYOfPools()

# @tool
# def getTVLOfDefiProject(question: str) -> str:
#     """ "useful when you need get TVL and info of defi project. The input to this should be a complete question about tvl."""
#     # agent = tvlPotocols.create_agent()
#     agent = tvlPotocols.create_agent().with_config(
#         {"configurable": {"llm": "openai_gpt_4_turbo_preview"}}
#     )
#     excutor = AgentExecutor(
#         agent=agent,
#         tools=tvlPotocols.tools,
#         verbose=True,
#     )
#     result = excutor.invoke({"input": question})
#     return result["output"]

# @tool
# def fetchTVLOfDefiProject(question: str) -> str:
#     """ "useful when you need fetch TVL and info of defi project."""
#     tvlPotocols.fetch()
#     return getTVLOfDefiProject(question)

# @tool
# def getCirculatingVolumeOfStablecoin(question: str) -> str:
#     """ "useful when you need get circulating volume of stablecoin. The input to this should be a complete question about circulating volume."""
#     # agent = tvlPotocols.create_agent()
#     agent = cvOfSc.create_agent().with_config(
#         {"configurable": {"llm": "openai_gpt_4_turbo_preview"}}
#     )
#     excutor = AgentExecutor(
#         agent=agent,
#         tools=cvOfSc.tools,
#         verbose=True,
#     )
#     result = excutor.invoke({"input": question})
#     return result["output"]

# @tool
# def fetchCirculatingVolumeOfStablecoin(question: str) -> str:
#     """ "useful when you need fetch Circulating Volume of stablecoin."""
#     cvOfSc.fetch()
#     return getCirculatingVolumeOfStablecoin(question)

# @tool
# def getTotalCirculatingVolumeOfStablecoin(question: str) -> str:
#     """ "useful when you need get the volume of fait currency pegged to the chain. The input to this should be a complete question about volume of fait currency pegged."""
#     # agent = tvlPotocols.create_agent()
#     agent = tcvOfSc.create_agent().with_config(
#         {"configurable": {"llm": "openai_gpt_4_turbo_preview"}}
#     )
#     excutor = AgentExecutor(
#         agent=agent,
#         tools=tcvOfSc.tools,
#         verbose=True,
#     )
#     result = excutor.invoke({"input": question})
#     return result["output"]

# @tool
# def fetchTotalCirculatingVolumeOfStablecoin(question: str) -> str:
#     """ "useful when you need fetch the volume of fait currency pegged to."""
#     tcvOfSc.fetch()
#     return getTotalCirculatingVolumeOfStablecoin(question)

# @tool
# def getYieldsAndAPYOfPools(question: str) -> str:
#     """ "useful when you need get yields or APY of defi pools. The input to this should be a complete question about yields or APY."""
#     # agent = tvlPotocols.create_agent()
#     agent = apyOfPools.create_agent().with_config(
#         {"configurable": {"llm": "openai_gpt_4_turbo_preview"}}
#     )
#     excutor = AgentExecutor(
#         agent=agent,
#         tools=apyOfPools.tools,
#         verbose=True,
#     )
#     result = excutor.invoke({"input": question})
#     return result["output"]

# @tool
# def fetchYieldsAndAPYOfPools(question: str) -> str:
#     """useful when you need fetch yields or APY of defi pools."""
#     apyOfPools.fetch()
#     return getYieldsAndAPYOfPools(question)

# from defillama_wrapper import DefiLLamaWrapInfoOfBridges

# infoOfBridges = DefiLLamaWrapInfoOfBridges()

# @tool
# def getInfoOfBridges(question: str) -> str:
#     """useful when you need get info of a cross-chain bridges. The input to this should be a complete question about cross-chain bridge."""
#     # agent = tvlPotocols.create_agent()
#     agent = infoOfBridges.create_agent().with_config(
#         {"configurable": {"llm": "openai_gpt_4_turbo_preview"}}
#     )
#     excutor = AgentExecutor(
#         agent=agent,
#         tools=infoOfBridges.tools,
#         verbose=True,
#     )
#     result = excutor.invoke({"input": question})
#     return result["output"]

# @tool
# def fetchInfoOfBridges(question: str) -> str:
#     """useful when you need fetch info of a cross-chain bridges."""
#     infoOfBridges.fetch()
#     return getInfoOfBridges(question)

# from defillama_wrapper import DefiLLamaWrapVolumeOfDex

# vOfDex = DefiLLamaWrapVolumeOfDex()

# @tool
# def getVolumeOfDex(question: str) -> str:
#     """useful when you need get volume of a Dex. The input to this should be a complete question about dex's volume."""
#     # agent = tvlPotocols.create_agent()
#     agent = vOfDex.create_agent().with_config(
#         {"configurable": {"llm": "openai_gpt_4_turbo_preview"}}
#     )
#     excutor = AgentExecutor(
#         agent=agent,
#         tools=vOfDex.tools,
#         verbose=True,
#     )
#     result = excutor.invoke({"input": question})
#     return result["output"]

# @tool
# def fetchVolumeOfDex(question: str) -> str:
#     """useful when you need fetch volume of a dex."""
#     vOfDex.fetch()
#     return getVolumeOfDex(question)

tools = [
    googleSerperSearch,
    # getHTMLFromURL,
    # getHTMLFromURLs,
    # getContentFromURL,
    # getContentOfURL,
    # getTVLOfDefiProject,
    # fetchTVLOfDefiProject,
    # getCirculatingVolumeOfStablecoin,
    # fetchCirculatingVolumeOfStablecoin,
    # getTotalCirculatingVolumeOfStablecoin,
    # fetchTotalCirculatingVolumeOfStablecoin,
    # getYieldsAndAPYOfPools,
    # fetchYieldsAndAPYOfPools,
    # getInfoOfBridges,
    # fetchInfoOfBridges,
    # getVolumeOfDex,
    # fetchVolumeOfDex,
    Tool(
        name="CryptocurrencyLatestQuote",
        func=cmc_last_quote_api.run,
        description="""useful when you need get a cryptocurrency's latest quote. The input to this should be a single cryptocurrency's symbol.""",
        coroutine=cmc_last_quote_api.arun,
    ),
    # Tool(
    #     name="TrendingLatest",
    #     func=cmc_trending_latest_api.run,
    #     description="""useful when you need get a list of all trending cryptocurrency market data, determined and sorted by CoinMarketCap search volume. The input to this should be a complete question in English, and the question must have a ranking requirement, and the ranking cannot exceed 20.""",
    #     coroutine=cmc_trending_latest_api.arun,
    # ),
    # Tool(
    #     name="TrendingGainersAndLosers",
    #     func=cmc_trending_gainers_losers_api.run,
    #     description="""useful when you need get a list of all trending cryptocurrencies, determined and sorted by the largest price gains or losses. The input to this should be a complete question in English, and the question must have a ranking requirement, and the ranking cannot exceed 20.""",
    #     coroutine=cmc_trending_gainers_losers_api.arun,
    # ),
    # Tool(
    #     name="TrendingMostVisited",
    #     func=cmc_trending_most_visited_api.run,
    #     description="""useful when you need get a list of all trending cryptocurrency market data, determined and sorted by traffic to coin detail pages. The input to this should be a complete question in English, and the question must have a ranking requirement, and the ranking cannot exceed 20.""",
    #     coroutine=cmc_trending_most_visited_api.arun,
    # ),
    # Tool(
    #     name="MetaDataOfCryptocurrency",
    #     func=cmc_metadata_api.run,
    #     description="""useful when you need get all static metadata available for one or more cryptocurrencies. The input to this should be a complete question in English.""",
    #     coroutine=cmc_metadata_api.arun,
    # ),
    getTokenMetadata,
    Tool(
        name="BuyOrSellSignal",
        func=tradingview.buySellSignal,
        description="""Useful when you need to know buy and sell signals for a cryptocurrency. The input to this should be a cryptocurrency's symbol.""",
        coroutine=tradingview.abuySellSignal,
    ),
    arxiv_search,
    arxiv_load,
]
