import asyncio
import json
import time
import sys
import threading
import time
from contextlib import asynccontextmanager
from json import JSONDecodeError
from typing import (
    AsyncGenerator,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    Optional,
    Tuple,
    Union,
    overload,
)
from urllib.parse import urlencode, urlsplit, urlunsplit

import aiohttp
import requests
from rebyte.rebyte_response import RebyteResponse
from rebyte.logger import get_logger

logger = get_logger(__name__)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

TIMEOUT_SECS = 600
MAX_SESSION_LIFETIME_SECS = 180
MAX_CONNECTION_RETRIES = 2

# Has one attribute per thread, 'session'.
_thread_context = threading.local()

def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))

def _make_session() -> requests.Session:
    s = requests.Session()
    return s

def parse_stream_helper(line: bytes) -> Optional[str]:
    if line:
        if line.strip() == b"data: [DONE]":
            # return here will cause GeneratorExit exception in urllib3
            # and it will close http connection with TCP Reset
            return None
        if line.startswith(b"data:"):
            line = line[len(b"data:"):]
            return line.strip().decode("utf-8")
        else:
            return None
    return None


def parse_stream(rbody: Iterator[bytes]) -> Iterator[str]:
    for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line


async def parse_stream_async(rbody: aiohttp.StreamReader):
    async for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line

def parse_rebyte_error(error_data):
    error_type = error_data.get('type')
    message = error_data.get('message', 'An unknown error occurred')

    if error_type == "malformed_authorization_header_error":
        raise ValueError("Invalid ReByte API key.")
    elif error_type == "project_not_found":
        raise ValueError("Invalid Project ID.")
    elif error_type == "internal_server_error" and message.startswith("Unhandled internal server error: Error: Could not find app"):
        raise ValueError("Invalid Agent ID.")
    elif error_type is not None:
        raise ValueError(message)

class RebyteAPIRequestor:
    def __init__(
        self,
        key=None,
        api_base=None,
    ):
        self.api_base = api_base or "https://rebyte.ai"
        self.api_key = key

    def _check_polling_response(self, response: RebyteResponse, predicate: Callable[[RebyteResponse], bool]):
        if not predicate(response):
            return
        err = response.get_error()
        if err:
          raise err

    def _poll(
        self,
        method,
        url,
        until,
        failed,
        params = None,
        headers = None,
        interval = None,
        delay = None
    ) -> Tuple[Iterator[RebyteResponse], bool, str]:
        if delay:
            time.sleep(delay)

        response, b, api_key = self.request(method, url, params, headers)
        self._check_polling_response(response, failed)
        start_time = time.time()
        while not until(response):
            if time.time() - start_time > TIMEOUT_SECS:
                raise RuntimeError("Operation polling timed out.")

            time.sleep(interval or response.retry_after or 10)
            response, b, api_key = self.request(method, url, params, headers)
            self._check_polling_response(response, failed)
        return response, b, api_key

    async def _apoll(
        self,
        method,
        url,
        until,
        failed,
        params = None,
        headers = None,
        interval = None,
        delay = None
    ) -> Tuple[Iterator[RebyteResponse], bool, str]:
        if delay:
            await asyncio.sleep(delay)

        response, b, api_key = await self.arequest(method, url, params, headers)
        self._check_polling_response(response, failed)
        start_time = time.time()
        while not until(response):
            if time.time() - start_time > TIMEOUT_SECS:
                raise RuntimeError("Operation polling timed out.")
            await asyncio.sleep(interval or response.retry_after or 10)
            response, b, api_key = await self.arequest(method, url, params, headers)
            self._check_polling_response(response, failed)
        return response, b, api_key

    @overload
    def request(
        self,
        method,
        url,
        params,
        headers,
        files,
        stream: Literal[True],
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Iterator[RebyteResponse], bool, str]:
        pass

    @overload
    def request(
        self,
        method,
        url,
        params=...,
        headers=...,
        files=...,
        *,
        stream: Literal[True],
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Iterator[RebyteResponse], bool, str]:
        pass

    @overload
    def request(
        self,
        method,
        url,
        params=...,
        headers=...,
        files=...,
        stream: Literal[False] = ...,
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[RebyteResponse, bool, str]:
        pass

    @overload
    def request(
        self,
        method,
        url,
        params=...,
        headers=...,
        files=...,
        stream: bool = ...,
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Union[RebyteResponse, Iterator[RebyteResponse]], bool, str]:
        pass

    def request(
        self,
        method,
        url,
        params=None,
        headers=None,
        files=None,
        stream: bool = False,
        request_id: Optional[str] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> Tuple[Union[RebyteResponse, Iterator[RebyteResponse]], bool, str]:
        result = self.request_raw(
            method.lower(),
            url,
            params=params,
            supplied_headers=headers,
            files=files,
            stream=stream,
            request_id=request_id,
            request_timeout=request_timeout,
        )
        resp, got_stream = self._interpret_response(result, stream)
        
        if isinstance(resp, RebyteResponse) and hasattr(resp, 'data') and 'error' in resp.data:
            logger.error(resp.data['error'].get('message', 'An unknown error occurred'))
            parse_rebyte_error(resp.data['error'])
        
        return resp, got_stream, self.api_key

    @overload
    async def arequest(
        self,
        method,
        url,
        params,
        headers,
        files,
        stream: Literal[True],
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[AsyncGenerator[RebyteResponse, None], bool, str]:
        pass

    @overload
    async def arequest(
        self,
        method,
        url,
        params=...,
        headers=...,
        files=...,
        *,
        stream: Literal[True],
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[AsyncGenerator[RebyteResponse, None], bool, str]:
        pass

    @overload
    async def arequest(
        self,
        method,
        url,
        params=...,
        headers=...,
        files=...,
        stream: Literal[False] = ...,
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[RebyteResponse, bool, str]:
        pass

    @overload
    async def arequest(
        self,
        method,
        url,
        params=...,
        headers=...,
        files=...,
        stream: bool = ...,
        request_id: Optional[str] = ...,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Union[RebyteResponse, AsyncGenerator[RebyteResponse, None]], bool, str]:
        pass

    async def arequest(
        self,
        method,
        url,
        params=None,
        headers=None,
        files=None,
        stream: bool = False,
        request_id: Optional[str] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> Tuple[Union[RebyteResponse, AsyncGenerator[RebyteResponse, None]], bool, str]:
        ctx = aiohttp_session()
        session = await ctx.__aenter__()
        try:
            result = await self.arequest_raw(
                method.lower(),
                url,
                session,
                params=params,
                supplied_headers=headers,
                files=files,
                request_id=request_id,
                request_timeout=request_timeout,
            )
            resp, got_stream = await self._interpret_async_response(result, stream)

            if isinstance(resp, RebyteResponse) and hasattr(resp, 'data') and 'error' in resp.data:
                logger.error(resp.data['error'].get('message', 'An unknown error occurred'))
                parse_rebyte_error(resp.data['error'])

        except Exception:
            await ctx.__aexit__(None, None, None)
            raise
        if got_stream:

            async def wrap_resp():
                assert isinstance(resp, AsyncGenerator)
                try:
                    async for r in resp:
                        yield r
                finally:
                    await ctx.__aexit__(None, None, None)

            return wrap_resp(), got_stream, self.api_key
        else:
            await ctx.__aexit__(None, None, None)
            return resp, got_stream, self.api_key

    def request_headers(
        self, method: str, extra, request_id: Optional[str]
    ) -> Dict[str, str]:
        user_agent = "Rebyte/v1 Python"
        headers = {
            "User-Agent": user_agent,
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        return headers

    def _validate_headers(
        self, supplied_headers: Optional[Dict[str, str]]
    ) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if supplied_headers is None:
            return headers

        if not isinstance(supplied_headers, dict):
            raise TypeError("Headers must be a dictionary")

        for k, v in supplied_headers.items():
            if not isinstance(k, str):
                raise TypeError("Header keys must be strings")
            if not isinstance(v, str):
                raise TypeError("Header values must be strings")
            headers[k] = v
        return headers

    def _prepare_request_raw(
        self,
        url,
        supplied_headers,
        method,
        params,
        files,
        request_id: Optional[str],
    ) -> Tuple[str, Dict[str, str], Optional[bytes]]:
        abs_url = "%s%s" % (self.api_base, url)
        headers = self._validate_headers(supplied_headers)

        data = None
        if method == "get" or method == "delete":
            if params:
                encoded_params = urlencode(
                    [(k, v) for k, v in params.items() if v is not None]
                )
                abs_url = _build_api_url(abs_url, encoded_params)
        elif method in {"post", "put"}:
            if params and files:
                data = params
            if params and not files:
                data = json.dumps(params).encode()
                headers["Content-Type"] = "application/json"
        else:
            raise "Unrecognized HTTP method"

        headers = self.request_headers(method, headers, request_id)
        return abs_url, headers, data

    def request_raw(
        self,
        method,
        url,
        *,
        params=None,
        supplied_headers: Optional[Dict[str, str]] = None,
        files=None,
        stream: bool = False,
        request_id: Optional[str] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> requests.Response:
        abs_url, headers, data = self._prepare_request_raw(
            url, supplied_headers, method, params, files, request_id
        )

        if not hasattr(_thread_context, "session"):
            _thread_context.session = _make_session()
            _thread_context.session_create_time = time.time()
        elif (
            time.time() - getattr(_thread_context, "session_create_time", 0)
            >= MAX_SESSION_LIFETIME_SECS
        ):
            _thread_context.session.close()
            _thread_context.session = _make_session()
            _thread_context.session_create_time = time.time()
        try:
            result = _thread_context.session.request(
                method,
                abs_url,
                headers=headers,
                data=data,
                files=files,
                stream=stream,
                timeout=request_timeout if request_timeout else TIMEOUT_SECS,
                proxies=_thread_context.session.proxies,
            )
        except requests.exceptions.Timeout as e:
            logger.error("Request timed out: {}".format(e))
            raise RuntimeError("Request timed out: {}".format(e))
        except requests.exceptions.RequestException as e:
            logger.error("Error communicating with Rebyte: {}".format(e))
            raise RuntimeError("Error communicating with Rebyte: {}".format(e))
        return result

    async def arequest_raw(
        self,
        method,
        url,
        session,
        *,
        params=None,
        supplied_headers: Optional[Dict[str, str]] = None,
        files=None,
        request_id: Optional[str] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> aiohttp.ClientResponse:
        abs_url, headers, data = self._prepare_request_raw(
            url, supplied_headers, method, params, files, request_id
        )

        if isinstance(request_timeout, tuple):
            timeout = aiohttp.ClientTimeout(
                connect=request_timeout[0],
                total=request_timeout[1],
            )
        else:
            timeout = aiohttp.ClientTimeout(
                total=request_timeout if request_timeout else TIMEOUT_SECS
            )

        if files:
            # TODO: Use `aiohttp.MultipartWriter` to create the multipart form data here.
            # For now we use the private `requests` method that is known to have worked so far.
            data, content_type = requests.models.RequestEncodingMixin._encode_files(  # type: ignore
                files, data
            )
            headers["Content-Type"] = content_type
        request_kwargs = {
            "method": method,
            "url": abs_url,
            "headers": headers,
            "data": data,
            "timeout": timeout,
        }
        try:
            result = await session.request(**request_kwargs)
            return result
        except (aiohttp.ServerTimeoutError, asyncio.TimeoutError) as e:
            logger.error("Request timed out: {}".format(e))
            raise RuntimeError("Request timed out: {}".format(e))
        except aiohttp.ClientError as e:
            logger.error("Error communicating with Rebyte: {}".format(e))
            raise RuntimeError("Error communicating with Rebyte: {}".format(e))

    def _interpret_response(
        self, result: requests.Response, stream: bool
    ) -> Tuple[Union[RebyteResponse, Iterator[RebyteResponse]], bool]:
        """Returns the response(s) and a bool indicating whether it is a stream."""
        if stream and "text/event-stream" in result.headers.get("Content-Type", ""):
            return (
                self._interpret_response_line(
                    line, result.status_code, result.headers, stream=True
                )
                for line in parse_stream(result.iter_lines())
            ), True
        else:
            return (
                self._interpret_response_line(
                    result.content.decode("utf-8"),
                    result.status_code,
                    result.headers,
                    stream=False,
                ),
                False,
            )

    async def _interpret_async_response(
        self, result: aiohttp.ClientResponse, stream: bool
    ) -> Tuple[Union[RebyteResponse, AsyncGenerator[RebyteResponse, None]], bool]:
        """Returns the response(s) and a bool indicating whether it is a stream."""
        if stream and "text/event-stream" in result.headers.get("Content-Type", ""):
            return (
                self._interpret_response_line(
                    line, result.status, result.headers, stream=True
                )
                async for line in parse_stream_async(result.content)
            ), True
        else:
            try:
                await result.read()
            except (aiohttp.ServerTimeoutError, asyncio.TimeoutError) as e:
                raise RuntimeError("Request timed out: {}".format(e))
            except aiohttp.ClientError as e:
                raise RuntimeError("Client error: {}".format(e))
            return (
                self._interpret_response_line(
                    (await result.read()).decode("utf-8"),
                    result.status,
                    result.headers,
                    stream=False,
                ),
                False,
            )

    def _interpret_response_line(
        self, rbody: str, rcode: int, rheaders, stream: bool
    ) -> RebyteResponse:
        try:
            if 'text/plain' in rheaders.get('Content-Type', ''):
                data = rbody
            else:
                data = json.loads(rbody)
        except (JSONDecodeError, UnicodeDecodeError) as e:
            raise f"HTTP code {rcode} from API ({rbody})"
        resp = RebyteResponse(data, rheaders, stream)
        if stream and resp.get_stream_error():
            raise resp.get_stream_error()
        return resp


@asynccontextmanager
async def aiohttp_session() -> AsyncIterator[aiohttp.ClientSession]:
    async with aiohttp.ClientSession() as session:
        yield session
        
