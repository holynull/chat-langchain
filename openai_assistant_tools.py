from typing import Any, Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup
import requests
from langchain_core.pydantic_v1 import BaseModel, root_validator
from typing_extensions import Literal

from langchain.utils import get_from_dict_or_env
from tradingview_ta import TA_Handler, Interval, Exchange


class GoogleSerperAPIWrapper(BaseModel):
    """Wrapper around the Serper.dev Google Search API.

    You can create a free API key at https://serper.dev.

    To use, you should have the environment variable ``SERPER_API_KEY``
    set with your API key, or pass `serper_api_key` as a named parameter
    to the constructor.

    Example:
        .. code-block:: python

            from langchain.utilities import GoogleSerperAPIWrapper
            google_serper = GoogleSerperAPIWrapper()
    """

    k: int = 10
    gl: str = "us"
    hl: str = "en"
    # "places" and "images" is available from Serper but not implemented in the
    # parser of run(). They can be used in results()
    type: Literal["news", "search", "places", "images"] = "search"
    result_key_for_type = {
        "news": "news",
        "places": "places",
        "images": "images",
        "search": "organic",
    }

    tbs: Optional[str] = None
    serper_api_key: Optional[str] = None
    aiosession: Optional[aiohttp.ClientSession] = None

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        serper_api_key = get_from_dict_or_env(
            values, "serper_api_key", "SERPER_API_KEY"
        )
        values["serper_api_key"] = serper_api_key

        return values

    def results(self, query: str, **kwargs: Any) -> Dict:
        """Run query through GoogleSearch."""
        return self._google_serper_api_results(
            query,
            gl=self.gl,
            hl=self.hl,
            num=self.k,
            tbs=self.tbs,
            search_type=self.type,
            **kwargs,
        )

    def run(self, query: str, **kwargs: Any) -> str:
        """Run query through GoogleSearch and parse result."""
        results = self._google_serper_api_results(
            query,
            gl=self.gl,
            hl=self.hl,
            num=self.k,
            tbs=self.tbs,
            search_type=self.type,
            **kwargs,
        )

        return self._parse_results(results)

    async def aresults(self, query: str, **kwargs: Any) -> Dict:
        """Run query through GoogleSearch."""
        results = await self._async_google_serper_search_results(
            query,
            gl=self.gl,
            hl=self.hl,
            num=self.k,
            search_type=self.type,
            tbs=self.tbs,
            **kwargs,
        )
        return results

    async def arun(self, query: str, **kwargs: Any) -> str:
        """Run query through GoogleSearch and parse result async."""
        results = await self._async_google_serper_search_results(
            query,
            gl=self.gl,
            hl=self.hl,
            num=self.k,
            search_type=self.type,
            tbs=self.tbs,
            **kwargs,
        )

        return self._parse_results(results)

    def _parse_snippets(self, results: dict) -> List[str]:
        snippets = []

        if results.get("answerBox"):
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                return [answer_box.get("answer")]
            elif answer_box.get("snippet"):
                return [answer_box.get("snippet").replace("\n", " ")]
            elif answer_box.get("snippetHighlighted"):
                return answer_box.get("snippetHighlighted")

        if results.get("knowledgeGraph"):
            kg = results.get("knowledgeGraph", {})
            title = kg.get("title")
            entity_type = kg.get("type")
            if entity_type:
                snippets.append(f"{title}: {entity_type}.")
            description = kg.get("description")
            if description:
                snippets.append(description)
            for attribute, value in kg.get("attributes", {}).items():
                snippets.append(f"{title} {attribute}: {value}.")

        for result in results[self.result_key_for_type[self.type]][: self.k]:
            if "snippet" in result:
                snippets.append(
                    f"Title:{result['title']}\nSnippet:{result['snippet']}\nLink:{result['link']}\n"
                )
            for attribute, value in result.get("attributes", {}).items():
                snippets.append(f"{attribute}: {value}.")

        if len(snippets) == 0:
            return ["No good Google Search Result was found"]
        return snippets

    def _parse_results(self, results: dict) -> str:
        return " ".join(self._parse_snippets(results))

    def _google_serper_api_results(
        self, search_term: str, search_type: str = "search", **kwargs: Any
    ) -> dict:
        headers = {
            "X-API-KEY": self.serper_api_key or "",
            "Content-Type": "application/json",
        }
        params = {
            "q": search_term,
            **{key: value for key, value in kwargs.items() if value is not None},
        }
        response = requests.post(
            f"https://google.serper.dev/{search_type}", headers=headers, params=params
        )
        response.raise_for_status()
        search_results = response.json()
        return search_results

    async def _async_google_serper_search_results(
        self, search_term: str, search_type: str = "search", **kwargs: Any
    ) -> dict:
        headers = {
            "X-API-KEY": self.serper_api_key or "",
            "Content-Type": "application/json",
        }
        url = f"https://google.serper.dev/{search_type}"
        params = {
            "q": search_term,
            **{key: value for key, value in kwargs.items() if value is not None},
        }

        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, params=params, headers=headers, raise_for_status=False
                ) as response:
                    search_results = await response.json()
        else:
            async with self.aiosession.post(
                url, params=params, headers=headers, raise_for_status=True
            ) as response:
                search_results = await response.json()

        return search_results


"""Lightweight wrapper around requests library, with async support."""
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional

import aiohttp
import requests
from langchain_core.pydantic_v1 import BaseModel, Extra


class Requests(BaseModel):
    """Wrapper around requests to handle auth and async.

    The main purpose of this wrapper is to handle authentication (by saving
    headers) and enable easy async methods on the same base object.
    """

    headers: Optional[Dict[str, str]] = None
    aiosession: Optional[aiohttp.ClientSession] = None
    auth: Optional[Any] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """GET the URL and return the text."""
        return requests.get(url, headers=self.headers, auth=self.auth, **kwargs)

    def post(self, url: str, data: Dict[str, Any], **kwargs: Any) -> requests.Response:
        """POST to the URL and return the text."""
        return requests.post(
            url, json=data, headers=self.headers, auth=self.auth, **kwargs
        )

    def patch(self, url: str, data: Dict[str, Any], **kwargs: Any) -> requests.Response:
        """PATCH the URL and return the text."""
        return requests.patch(
            url, json=data, headers=self.headers, auth=self.auth, **kwargs
        )

    def put(self, url: str, data: Dict[str, Any], **kwargs: Any) -> requests.Response:
        """PUT the URL and return the text."""
        return requests.put(
            url, json=data, headers=self.headers, auth=self.auth, **kwargs
        )

    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        """DELETE the URL and return the text."""
        return requests.delete(url, headers=self.headers, auth=self.auth, **kwargs)

    @asynccontextmanager
    async def _arequest(
        self, method: str, url: str, **kwargs: Any
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        """Make an async request."""
        if not self.aiosession:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False), trust_env=True
            ) as session:
                async with session.request(
                    method, url, headers=self.headers, auth=self.auth, **kwargs
                ) as response:
                    yield response
        else:
            async with self.aiosession.request(
                method, url, headers=self.headers, auth=self.auth, **kwargs
            ) as response:
                yield response

    @asynccontextmanager
    async def aget(
        self, url: str, **kwargs: Any
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        """GET the URL and return the text asynchronously."""
        async with self._arequest("GET", url, **kwargs) as response:
            yield response

    @asynccontextmanager
    async def apost(
        self, url: str, data: Dict[str, Any], **kwargs: Any
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        """POST to the URL and return the text asynchronously."""
        async with self._arequest("POST", url, json=data, **kwargs) as response:
            yield response

    @asynccontextmanager
    async def apatch(
        self, url: str, data: Dict[str, Any], **kwargs: Any
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        """PATCH the URL and return the text asynchronously."""
        async with self._arequest("PATCH", url, json=data, **kwargs) as response:
            yield response

    @asynccontextmanager
    async def aput(
        self, url: str, data: Dict[str, Any], **kwargs: Any
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        """PUT the URL and return the text asynchronously."""
        async with self._arequest("PUT", url, json=data, **kwargs) as response:
            yield response

    @asynccontextmanager
    async def adelete(
        self, url: str, **kwargs: Any
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        """DELETE the URL and return the text asynchronously."""
        async with self._arequest("DELETE", url, **kwargs) as response:
            yield response


class TextRequestsWrapper(BaseModel):
    """Lightweight wrapper around requests library.

    The main purpose of this wrapper is to always return a text output.
    """

    headers: Optional[Dict[str, str]] = None
    aiosession: Optional[aiohttp.ClientSession] = None
    auth: Optional[Any] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def requests(self) -> Requests:
        return Requests(
            headers=self.headers, aiosession=self.aiosession, auth=self.auth
        )

    def get(self, url: str, **kwargs: Any) -> str:
        """GET the URL and return the text."""
        return self.requests.get(url, **kwargs).text

    def post(self, url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        """POST to the URL and return the text."""
        return self.requests.post(url, data, **kwargs).text

    def patch(self, url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        """PATCH the URL and return the text."""
        return self.requests.patch(url, data, **kwargs).text

    def put(self, url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        """PUT the URL and return the text."""
        return self.requests.put(url, data, **kwargs).text

    def delete(self, url: str, **kwargs: Any) -> str:
        """DELETE the URL and return the text."""
        return self.requests.delete(url, **kwargs).text

    async def aget(self, url: str, **kwargs: Any) -> str:
        """GET the URL and return the text asynchronously."""
        async with self.requests.aget(url, **kwargs) as response:
            return await response.text()

    async def apost(self, url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        """POST to the URL and return the text asynchronously."""
        async with self.requests.apost(url, data, **kwargs) as response:
            return await response.text()

    async def apatch(self, url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        """PATCH the URL and return the text asynchronously."""
        async with self.requests.apatch(url, data, **kwargs) as response:
            return await response.text()

    async def aput(self, url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        """PUT the URL and return the text asynchronously."""
        async with self.requests.aput(url, data, **kwargs) as response:
            return await response.text()

    async def adelete(self, url: str, **kwargs: Any) -> str:
        """DELETE the URL and return the text asynchronously."""
        async with self.requests.adelete(url, **kwargs) as response:
            return await response.text()


# For backwards compatibility
# RequestsWrapper = TextRequestsWrapper

"""Chain that makes API calls and summarizes the responses to answer a question."""
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate,PromptTemplate
from langchain_core.pydantic_v1 import Field, root_validator

from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain.chains.api.prompt import API_RESPONSE_PROMPT, API_URL_PROMPT
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain


def _extract_scheme_and_domain(url: str) -> Tuple[str, str]:
    """Extract the scheme + domain from a given URL.

    Args:
        url (str): The input URL.

    Returns:
        return a 2-tuple of scheme and domain
    """
    parsed_uri = urlparse(url)
    return parsed_uri.scheme, parsed_uri.netloc


def _check_in_allowed_domain(url: str, limit_to_domains: Sequence[str]) -> bool:
    """Check if a URL is in the allowed domains.

    Args:
        url (str): The input URL.
        limit_to_domains (Sequence[str]): The allowed domains.

    Returns:
        bool: True if the URL is in the allowed domains, False otherwise.
    """
    scheme, domain = _extract_scheme_and_domain(url)

    for allowed_domain in limit_to_domains:
        allowed_scheme, allowed_domain = _extract_scheme_and_domain(allowed_domain)
        if scheme == allowed_scheme and domain == allowed_domain:
            return True
    return False


class MyAPIChain(Chain):
    """Chain that makes API calls and summarizes the responses to answer a question.

    *Security Note*: This API chain uses the requests toolkit
        to make GET, POST, PATCH, PUT, and DELETE requests to an API.

        Exercise care in who is allowed to use this chain. If exposing
        to end users, consider that users will be able to make arbitrary
        requests on behalf of the server hosting the code. For example,
        users could ask the server to make a request to a private API
        that is only accessible from the server.

        Control access to who can submit issue requests using this toolkit and
        what network access it has.

        See https://python.langchain.com/docs/security for more information.
    """

    api_request_chain: LLMChain
    api_answer_chain: LLMChain
    requests_wrapper: TextRequestsWrapper = Field(exclude=True)
    api_docs: str
    question_key: str = "question"  #: :meta private:
    output_key: str = "output"  #: :meta private:
    limit_to_domains: Optional[Sequence[str]]
    """Use to limit the domains that can be accessed by the API chain.
    
    * For example, to limit to just the domain `https://www.example.com`, set
        `limit_to_domains=["https://www.example.com"]`.
        
    * The default value is an empty tuple, which means that no domains are
      allowed by default. By design this will raise an error on instantiation.
    * Use a None if you want to allow all domains by default -- this is not
      recommended for security reasons, as it would allow malicious users to
      make requests to arbitrary URLS including internal APIs accessible from
      the server.
    """

    @property
    def input_keys(self) -> List[str]:
        """Expect input key.

        :meta private:
        """
        return [self.question_key]

    @property
    def output_keys(self) -> List[str]:
        """Expect output key.

        :meta private:
        """
        return [self.output_key]

    @root_validator(pre=True)
    def validate_api_request_prompt(cls, values: Dict) -> Dict:
        """Check that api request prompt expects the right variables."""
        input_vars = values["api_request_chain"].prompt.input_variables
        expected_vars = {"question", "api_docs"}
        if set(input_vars) != expected_vars:
            raise ValueError(
                f"Input variables should be {expected_vars}, got {input_vars}"
            )
        return values

    @root_validator(pre=True)
    def validate_limit_to_domains(cls, values: Dict) -> Dict:
        """Check that allowed domains are valid."""
        if "limit_to_domains" not in values:
            raise ValueError(
                "You must specify a list of domains to limit access using "
                "`limit_to_domains`"
            )
        if not values["limit_to_domains"] and values["limit_to_domains"] is not None:
            raise ValueError(
                "Please provide a list of domains to limit access using "
                "`limit_to_domains`."
            )
        return values

    @root_validator(pre=True)
    def validate_api_answer_prompt(cls, values: Dict) -> Dict:
        """Check that api answer prompt expects the right variables."""
        input_vars = values["api_answer_chain"].prompt.input_variables
        expected_vars = {"question", "api_docs", "api_url", "api_response"}
        if set(input_vars) != expected_vars:
            raise ValueError(
                f"Input variables should be {expected_vars}, got {input_vars}"
            )
        return values

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        question = inputs[self.question_key]
        api_url = self.api_request_chain.predict(
            question=question,
            api_docs=self.api_docs,
            callbacks=_run_manager.get_child(),
        )
        _run_manager.on_text(api_url, color="green", end="\n", verbose=self.verbose)
        api_url = api_url.strip()
        if self.limit_to_domains and not _check_in_allowed_domain(
            api_url, self.limit_to_domains
        ):
            raise ValueError(
                f"{api_url} is not in the allowed domains: {self.limit_to_domains}"
            )
        api_response = self.requests_wrapper.get(api_url)
        _run_manager.on_text(
            api_response, color="yellow", end="\n", verbose=self.verbose
        )
        answer = self.api_answer_chain.predict(
            question=question,
            api_docs=self.api_docs,
            api_url=api_url,
            api_response=api_response,
            callbacks=_run_manager.get_child(),
        )
        return {self.output_key: answer}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or AsyncCallbackManagerForChainRun.get_noop_manager()
        question = inputs[self.question_key]
        api_url = await self.api_request_chain.apredict(
            question=question,
            api_docs=self.api_docs,
            callbacks=_run_manager.get_child(),
        )
        await _run_manager.on_text(
            api_url, color="green", end="\n", verbose=self.verbose
        )
        api_url = api_url.strip()
        if self.limit_to_domains and not _check_in_allowed_domain(
            api_url, self.limit_to_domains
        ):
            raise ValueError(
                f"{api_url} is not in the allowed domains: {self.limit_to_domains}"
            )
        api_response = await self.requests_wrapper.aget(api_url)
        await _run_manager.on_text(
            api_response, color="yellow", end="\n", verbose=self.verbose
        )
        answer = await self.api_answer_chain.apredict(
            question=question,
            api_docs=self.api_docs,
            api_url=api_url,
            api_response=api_response,
            callbacks=_run_manager.get_child(),
        )
        return {self.output_key: answer}

    @classmethod
    def from_llm_and_api_docs(
        cls,
        llm: BaseLanguageModel,
        api_docs: str,
        headers: Optional[dict] = None,
        api_url_prompt: BasePromptTemplate = API_URL_PROMPT,
        api_response_prompt: BasePromptTemplate = API_RESPONSE_PROMPT,
        limit_to_domains: Optional[Sequence[str]] = tuple(),
        **kwargs: Any,
    ) -> Chain:
        """Load chain from just an LLM and the api docs."""
        get_request_chain = LLMChain(llm=llm, prompt=api_url_prompt)
        requests_wrapper = TextRequestsWrapper(headers=headers)
        get_answer_chain = LLMChain(llm=llm, prompt=api_response_prompt)
        return cls(
            api_request_chain=get_request_chain,
            api_answer_chain=get_answer_chain,
            requests_wrapper=requests_wrapper,
            api_docs=api_docs,
            limit_to_domains=limit_to_domains,
            **kwargs,
        )

    @property
    def _chain_type(self) -> str:
        return "my_api_chain"


def getHTMLFromURL(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.prettify()


class TradingViewReasearchReportChain(Chain):
    """
    An example of a custom chain.
    """

    prompt: BasePromptTemplate
    """Prompt object to use."""
    llm: BaseLanguageModel
    output_key: str = "text"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Will be whatever keys the prompt expects.

        :meta private:
        """
        return self.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        """Will always return text key.

        :meta private:
        """
        return [self.output_key]

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # Your custom chain logic goes here
        # This is just an example that mimics LLMChain
        prompt_value = self.prompt.format_prompt(**inputs)
        if run_manager:
            run_manager.on_text(
                prompt_value.to_string(),
                color="green",
                end="\n",
                verbose=self.verbose,
            )
        # Whenever you call a language model, or another chain, you should pass
        # a callback manager to it. This allows the inner run to be tracked by
        # any callbacks that are registered on the outer run.
        # You can always obtain a callback manager for this by calling
        # `run_manager.get_child()` as shown below.
        response = self.llm.generate_prompt(
            [prompt_value], callbacks=run_manager.get_child() if run_manager else None
        )

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        # answer=self.answer_chain.run(question=inputs['user_input'],context=res)
        if run_manager:
            run_manager.on_text(
                response.generations[0][0].text,
                color="yellow",
                end="\n",
                verbose=self.verbose,
            )
        return {self.output_key: response.generations[0][0].text}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # Your custom chain logic goes here
        # This is just an example that mimics LLMChain
        prompt_value = self.prompt.format_prompt(**inputs)
        if run_manager:
            await run_manager.on_text(
                prompt_value.to_string(),
                color="green",
                end="\n",
                verbose=self.verbose,
            )
        # Whenever you call a language model, or another chain, you should pass
        # a callback manager to it. This allows the inner run to be tracked by
        # any callbacks that are registered on the outer run.
        # You can always obtain a callback manager for this by calling
        # `run_manager.get_child()` as shown below.
        response = await self.llm.agenerate_prompt(
            [prompt_value], callbacks=run_manager.get_child() if run_manager else None
        )

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            await run_manager.on_text(
                response.generations[0][0].text,
                color="yellow",
                end="\n",
                verbose=self.verbose,
            )
        return {self.output_key: response.generations[0][0].text}

    @property
    def _chain_type(self) -> str:
        return "indicators_questions_chain"

    @classmethod
    def from_llm(
        cls,
        llm,
        **kwargs: Any,
    ) -> Chain:
        PROMPT_TEMPLATE = """We have an unofficial python API wrapper to retrieve technical analysis from TradingView.
Retrieving the analysis:
- summary: Technical analysis (based on both oscillators and moving averages).
```
# Example
{{'RECOMMENDATION': 'BUY', 'BUY': 12, 'SELL': 7, 'NEUTRAL': 9}}
```
- oscillators: Technical analysis (based on oscillators).
```
# Example
{{'RECOMMENDATION': 'BUY', 'BUY': 2, 'SELL': 1, 'NEUTRAL': 8, 'COMPUTE': {{'RSI': 'NEUTRAL', 'STOCH.K': 'NEUTRAL', 'CCI': 'NEUTRAL', 'ADX': 'NEUTRAL', 'AO': 'NEUTRAL', 'Mom': 'BUY', 'MACD': 'SELL', 'Stoch.RSI': 'NEUTRAL', 'W%R': 'NEUTRAL', 'BBP': 'BUY', 'UO': 'NEUTRAL'}}}}
```
- moving_averages: Technical analysis (based on moving averages).
```
# Example
{{'RECOMMENDATION': 'BUY', 'BUY': 9, 'SELL': 5, 'NEUTRAL': 1, 'COMPUTE': {{'EMA10': 'SELL', 'SMA10': 'SELL', 'EMA20': 'SELL', 'SMA20': 'SELL', 'EMA30': 'BUY', 'SMA30': 'BUY', 'EMA50': 'BUY', 'SMA50': 'BUY', 'EMA100': 'BUY', 'SMA100': 'BUY', 'EMA200': 'BUY', 'SMA200': 'BUY', 'Ichimoku': 'NEUTRAL', 'VWMA': 'SELL', 'HullMA': 'BUY'}}}}
```
- indicators: Technical indicators.
```
# Example
{{'Recommend.Other': 0, 'Recommend.All': 0.26666667, 'Recommend.MA': 0.53333333, 'RSI': 60.28037412, 'RSI[1]': 58.58364778, 'Stoch.K': 73.80404453, 'Stoch.D': 79.64297643, 'Stoch.K[1]': 78.88160227, 'Stoch.D[1]': 85.97647064, 'CCI20': 46.58442886, 'CCI20[1]': 34.57058796, 'ADX': 35.78754863, 'ADX+DI': 23.16948389, 'ADX-DI': 13.82449817, 'ADX+DI[1]': 24.15991909, 'ADX-DI[1]': 13.87125505, 'AO': 6675.72158824, 'AO[1]': 7283.92420588, 'Mom': 1532.6, 'Mom[1]': 108.29, 'MACD.macd': 2444.73734978, 'MACD.signal': 2606.00138275, 'Rec.Stoch.RSI': 0, 'Stoch.RSI.K': 18.53740187, 'Rec.WR': 0, 'W.R': -26.05634845, 'Rec.BBPower': 0, 'BBPower': 295.52055898, 'Rec.UO': 0, 'UO': 55.68311917, 'close': 45326.97, 'EMA5': 45600.06414333, 'SMA5': 45995.592, 'EMA10': 45223.22433151, 'SMA10': 45952.635, 'EMA20': 43451.52018338, 'SMA20': 43609.214, 'EMA30': 41908.5944052, 'SMA30': 40880.391, 'EMA50': 40352.10222373, 'SMA50': 37819.3566, 'EMA100': 40356.09177879, 'SMA100': 38009.7808, 'EMA200': 39466.50411569, 'SMA200': 45551.36135, 'Rec.Ichimoku': 0, 'Ichimoku.BLine': 40772.57, 'Rec.VWMA': 1, 'VWMA': 43471.81729377, 'Rec.HullMA9': -1, 'HullMA9': 45470.37107407, 'Pivot.M.Classic.S3': 11389.27666667, 'Pivot.M.Classic.S2': 24559.27666667, 'Pivot.M.Classic.S1': 33010.55333333, 'Pivot.M.Classic.Middle': 37729.27666667, 'Pivot.M.Classic.R1': 46180.55333333, 'Pivot.M.Classic.R2': 50899.27666667, 'Pivot.M.Classic.R3': 64069.27666667, 'Pivot.M.Fibonacci.S3': 24559.27666667, 'Pivot.M.Fibonacci.S2': 29590.21666667, 'Pivot.M.Fibonacci.S1': 32698.33666667, 'Pivot.M.Fibonacci.Middle': 37729.27666667, 'Pivot.M.Fibonacci.R1': 42760.21666667, 'Pivot.M.Fibonacci.R2': 45868.33666667, 'Pivot.M.Fibonacci.R3': 50899.27666667, 'Pivot.M.Camarilla.S3': 37840.08, 'Pivot.M.Camarilla.S2': 39047.33, 'Pivot.M.Camarilla.S1': 40254.58, 'Pivot.M.Camarilla.Middle': 37729.27666667, 'Pivot.M.Camarilla.R1': 42669.08, 'Pivot.M.Camarilla.R2': 43876.33, 'Pivot.M.Camarilla.R3': 45083.58, 'Pivot.M.Woodie.S3': 21706.84, 'Pivot.M.Woodie.S2': 25492.42, 'Pivot.M.Woodie.S1': 34876.84, 'Pivot.M.Woodie.Middle': 38662.42, 'Pivot.M.Woodie.R1': 48046.84, 'Pivot.M.Woodie.R2': 51832.42, 'Pivot.M.Woodie.R3': 61216.84, 'Pivot.M.Demark.S1': 35369.915, 'Pivot.M.Demark.Middle': 38908.9575, 'Pivot.M.Demark.R1': 48539.915, 'open': 44695.95, 'P.SAR': 48068.64, 'BB.lower': 37961.23510877, 'BB.upper': 49257.19289123, 'AO[2]': 7524.31223529, 'volume': 32744.424503, 'change': 1.44612354, 'low': 44203.28, 'high': 45560}}
```

We got the analysis data of {symbol} from python-tradingview-ta as following:
summary:{summary}
oscillators:{oscillators}
moving_averages:{moving_averages}
indicators:{indicators}
"""
        PROMPT_TEMPLATE = (
            PROMPT_TEMPLATE
            + """\nPlease generate the analysis results by analyzing data the above, and provide the market trend. If the strength of the signal is represented by a score from 1 to 10, where a higher score indicates a stronger signal, please give a score to the strength of the signal in the end.
Your generation:
"""
        )

        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        return cls(llm=llm, prompt=prompt, **kwargs)



class TradingviewWrapper:
    llm: BaseLanguageModel

    def __init__(cls, llm):
        cls.llm = llm

    def buySellSignal(cls, symbol: str, **kwargs: any) -> str:
        btc_usdt = TA_Handler(
            symbol=f"{symbol}USDT",
            screener="crypto",
            exchange="GATEIO",
            interval=Interval.INTERVAL_1_DAY,
        )
        summary = btc_usdt.get_analysis().summary
        oscillators = btc_usdt.get_analysis().oscillators
        moving_averages = btc_usdt.get_analysis().moving_averages
        indicators = btc_usdt.get_analysis().indicators
        # return "\n".join([f"Summary:{summary}",f"Oscillators:{oscillators}",f"Moving Averages:{moving_averages}",f"Indicators:{indicators}"])
        tradingview_chain = TradingViewReasearchReportChain.from_llm(
            llm=cls.llm, verbose=True
        )
        return tradingview_chain.run(
            symbol=f"{symbol}/usdt",
            summary=summary,
            oscillators=oscillators,
            moving_averages=moving_averages,
            indicators=indicators,
        )

    async def abuySellSignal(cls, symbol: str, **kwargs: any) -> str:
        btc_usdt = TA_Handler(
            symbol=f"{symbol}USDT",
            screener="crypto",
            exchange="GATEIO",
            interval=Interval.INTERVAL_1_DAY,
        )
        summary = btc_usdt.get_analysis().summary
        oscillators = btc_usdt.get_analysis().oscillators
        moving_averages = btc_usdt.get_analysis().moving_averages
        indicators = btc_usdt.get_analysis().indicators
        # return "\n".join([f"Summary:{summary}",f"Oscillators:{oscillators}",f"Moving Averages:{moving_averages}",f"Indicators:{indicators}"])
        tradingview_chain = TradingViewReasearchReportChain.from_llm(
            llm=cls.llm, verbose=True
        )
        return await tradingview_chain.arun(
            symbol=f"{symbol}/usdt",
            summary=summary,
            oscillators=oscillators,
            moving_averages=moving_averages,
            indicators=indicators,
        )