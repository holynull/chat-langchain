from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
from langchain.agents import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from openai_assistant_tools import GoogleSerperAPIWrapper


def fetch_html(url: str) -> str:
    # 创建一个HTTP会话
    with requests.Session() as session:
        # 同步获取响应
        response = session.get(url)
        # 确保响应状态为200
        if response.status_code == 200:
            # 读取响应的文本内容
            html = response.text
            return html
        else:
            raise Exception(f"Error fetching '{url}': Status {response.status_code}")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def fetch_html_chromedriver(url: str) -> str:
    # 初始化配置对象
    chrome_options = Options()

    # 启用无头模式
    chrome_options.add_argument("--headless")

    # 禁用GPU加速（在某些情况下可以避免一些问题）
    chrome_options.add_argument("--disable-gpu")

    # 指定Chrome WebDriver的路径（如果已添加到环境变量，则不需要）
    driver_path = "chromedriver-mac-x64/chromedriver"
    service = Service(executable_path=driver_path)

    # 初始化WebDriver，并传入配置
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 打开网页
    driver.get(url=url)

    # 获取HTML内容
    html_content = driver.page_source

    # 关闭浏览器
    driver.quit()
    return html_content


def getCleanHTML(url: str) -> str:
    html_content = fetch_html_chromedriver(url=url)
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
            "title",
            "svg",
        ]:
            tag.decompose()
        if tag.attrs is not None and isinstance(tag.attrs, dict):
            tag.attrs = {
                key: value for key, value in tag.attrs.items() if key != "class"
            }

    # 可选：清理空白行
    clean_html = re.sub(r"(?m)^[\t ]+$", "", soup.prettify())
    return clean_html


@tool
def getContentOfURL(question: str) -> str:
    """Useful when you need to know as much as possible about the content of the page that the URL points to. The input must be a complete question about getting as much of the content of the page pointed to by the URL as possible, and must contain the URL."""
    # 定义URL的正则表达式
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    # 在字符串中搜索URL
    found_urls = re.findall(url_regex, question)

    # 检查是否找到了URL
    if found_urls:
        # 验证找到的第一个URL是否有效
        parsed_url = urlparse(found_urls[0])
        if bool(parsed_url.scheme) and bool(parsed_url.netloc):
            url = found_urls[0]
        else:
            raise ValueError("找到的URL无效")
    else:
        # 如果没有找到URL，抛出异常
        raise ValueError("字符串中不包含URL")
    try:
        html_content = getCleanHTML(url)
    except Exception as e:
        return f"When get the content of the link `{url}`, got an exception:{e}"

    llm = ChatOpenAI(
        temperature=0.9,
        model="gpt-4-turbo-preview",
        verbose=True,
        streaming=True,
    )
    prompt_template = """Because you are required to provide as much information to users as possible and answer users' questions. So, if you cannot get as much information as possible from the extracted HTML content to answer the user's question, return NEED_SEARCH. Otherwise, please return your answer.

URL:{url}
    
```html
{main_html}
```

Question:{question}

Answer:

"""
    prompt = ChatPromptTemplate.from_messages(
        [
            HumanMessagePromptTemplate.from_template(prompt_template),
            # MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    extract_chain = prompt | llm | StrOutputParser()
    answer = extract_chain.invoke(
        {"url": url, "main_html": html_content, "question": question}
    )
    if answer == "NEED_SEARCH":
        # 使用urlparse()函数解析URL
        # parsed_url = urlparse(url)

        # 获取域名
        # domain_end_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        search = GoogleSerperAPIWrapper()
        search_result = search.results(url)
        prompt_template = """URL:{url}

Data:
```json
{organic}
```
Since the content at that "{url}" could not be extracted, the "{url}" was searched using Google search. "Data" is the result of a Google search for "{url}". Please select a result that is highly relevant to the URL "{url}", but the `link` cannot be equal to "{url}", and return `link` of the result. Just return `link` without any hints.
"""
        prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template(prompt_template),
            ]
        )
        get_link_chain = prompt | llm | StrOutputParser()
        link = get_link_chain.invoke(
            {
                "url": url,
                "organic": [
                    item for item in search_result["organic"] if item["link"] != url
                ],
            }
        )
        try:
            main_html = getCleanHTML(link)
        except Exception as e:
            return (
                f"When get the content of a related link `{link}`, got an exception:{e}"
            )
        prompt_template = """Since you can't get as much information from extracting the content of the "{url}" link to answer the user's question. So you can answer as many users' questions as possible through the content of a related link, and provide some other related links for users' reference.

URL:{url}

Related Link:{related_link}

HTML of Related Link:
```html
{main_html}
```

Other Related Links: 
```json
{other_related_links}
```

Question:{question}

Answer:

"""
    prompt = ChatPromptTemplate.from_messages(
        [
            # SystemMessagePromptTemplate.from_template(
            #     "If using the search tool, prefix the string parameter with [S]."
            # ),
            HumanMessagePromptTemplate.from_template(prompt_template),
            # MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    extract_chain = prompt | llm | StrOutputParser()
    answer = extract_chain.invoke(
        {
            "url": url,
            "main_html": main_html,
            "related_link": link,
            "other_related_links": [
                item for item in search_result["organic"] if item["link"] != url
            ],
            "question": question,
        }
    )
    return answer


@tool
def getHTMLOfURL(url: str) -> str:
    """Useful when you need to get HTML of the URL point to. The input for this should be a complete URL."""

    try:
        html_content = getCleanHTML(url)
        print(html_content)
    except Exception as e:
        return f"When get the content of the link `{url}`, got an exception:{e}"

    llm = ChatOpenAI(
        temperature=0.9,
        model="gpt-4-turbo-preview",
        verbose=True,
        streaming=True,
    )
    prompt_template = """If you cannot get enough information from the extracted HTML content to help the user understand the content at the URL, return NEED_SEARCH. Otherwise, NO_NEED_SEARCH is returned.

URL:{url}
    
```html
{main_html}
```
Answer:

"""
    prompt = ChatPromptTemplate.from_messages(
        [
            HumanMessagePromptTemplate.from_template(prompt_template),
            # MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    extract_chain = prompt | llm | StrOutputParser()
    answer = extract_chain.invoke({"url": url, "main_html": html_content})
    if answer == "NEED_SEARCH":
        # 使用urlparse()函数解析URL
        # parsed_url = urlparse(url)

        # 获取域名
        # domain_end_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        search = GoogleSerperAPIWrapper()
        search_result = search.results(url)
        prompt_template = """URL:{url}

Data:
```json
{organic}
```
Since the content at that "{url}" could not be extracted, the "{url}" was searched using Google search. "Data" is the result of a Google search for "{url}". Please select a result that is highly relevant to the URL "{url}", but the `link` cannot be equal to "{url}", and return `link` of the result. Just return `link` without any hints.
"""
        prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template(prompt_template),
            ]
        )
        get_link_chain = prompt | llm | StrOutputParser()
        link = get_link_chain.invoke(
            {
                "url": url,
                "organic": [
                    item for item in search_result["organic"] if item["link"] != url
                ],
            }
        )
        try:
            main_html = getCleanHTML(link)
            return f"""Since the content of `{url}` could not be extracted, the HTML of the relevant link `{link}` was found through google search, as follows:
```html
{main_html}
```

Other Related Links:
```json
{
    [
        item for item in search_result["organic"] if item["link"] != url]
}
```
"""
        except Exception as e:
            return (
                f"When get the content of a related link `{link}`, got an exception:{e}"
            )
    else:
        return html_content
