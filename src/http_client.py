import logging
from typing import Tuple, Protocol, Dict
import aiohttp

from exceptions import (
    InvalidCredentials,
    ResourceNotFound,
    PlanUpgradeRequired,
    UnknownError,
)

logger = logging.getLogger(__name__)


class HTTPClientProtocol(Protocol):
    async def post(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, dict]:
        raise NotImplementedError()

    async def get(self, endpoint: str, headers: dict) -> Tuple[int, dict, dict]:
        raise NotImplementedError()

    async def patch(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, dict]:
        raise NotImplementedError()

    async def delete(self, endpoint: str, headers: dict) -> None:
        raise NotImplementedError()


class AsyncClient(HTTPClientProtocol):
    ERROR_PER_STATUS_CODE_MAP = {
        "401": InvalidCredentials,
        "404": ResourceNotFound,
        "402": PlanUpgradeRequired,
    }

    def __init__(self, host: str, bearer_token: str):
        self.bearer_token = bearer_token
        self.host = host

    async def post(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, dict]:
        async with self._build_session(headers) as s:
            async with s.post(endpoint, json=data) as result:
                status_code = result.status
                result_headers: Dict = dict(result.headers)
                response_body: Dict = await result.json()
                if status_code != 200:
                    error_type = self.ERROR_PER_STATUS_CODE_MAP.get(
                        str(status_code), UnknownError
                    )
                    raise error_type(
                        f"POST request to: {self.host}{endpoint} has returned with status code: {status_code}. "
                        f'Error: "{str(result.content)}"'
                    )

        return status_code, response_body, result_headers

    async def get(self, endpoint: str, headers: dict) -> Tuple[int, dict, dict]:
        async with self._build_session(headers) as s:
            async with s.get(endpoint) as result:
                status_code = result.status
                result_headers: Dict = dict(result.headers)
                response_body: Dict = await result.json()

                if status_code != 200:
                    error_type = self.ERROR_PER_STATUS_CODE_MAP.get(
                        str(status_code), UnknownError
                    )
                    raise error_type(
                        f"GET request to: {self.host}{endpoint} has returned with status code: {status_code}. "
                        f'Error: "{str(result.content)}"'
                    )

        return status_code, response_body, result_headers

    async def patch(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, dict]:
        async with self._build_session(headers) as s:
            async with s.patch(endpoint, json=data) as result:
                status_code = result.status
                result_headers: Dict = dict(result.headers)
                response_body: Dict = await result.json()

                if status_code != 204:
                    error_type = self.ERROR_PER_STATUS_CODE_MAP.get(
                        str(status_code), UnknownError
                    )
                    raise error_type(
                        f"PATCH request to: {self.host}{endpoint} has returned with status code: {status_code}. "
                        f'Error: "{str(result.content)}"'
                    )

        return status_code, response_body, result_headers

    async def delete(self, endpoint: str, headers: dict) -> None:
        async with self._build_session(headers) as s:
            async with s.delete(endpoint) as result:
                status_code = result.status
                if status_code != 204:
                    error_type = self.ERROR_PER_STATUS_CODE_MAP.get(
                        str(status_code), UnknownError
                    )
                    raise error_type(
                        f"DELETE request to: {self.host}{endpoint} has returned with status code: {status_code}. "
                        f'Error: "{str(result.content)}"'
                    )

    def _build_session(self, headers: dict) -> aiohttp.ClientSession:
        s = aiohttp.ClientSession(self.host)
        s.headers.update(headers)
        s.headers.update({"Authorization": f"Bearer {self.bearer_token}"})
        logger.debug(f"{len(headers) + 1} header(s) added to base session.")
        return s
