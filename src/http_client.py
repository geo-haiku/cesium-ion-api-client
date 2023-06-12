import logging
from typing import Tuple, Protocol, Dict
from requests_toolbelt.sessions import BaseUrlSession
from requests.structures import CaseInsensitiveDict

logger = logging.getLogger(__name__)


class HTTPClientProtocol(Protocol):
    def post(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, CaseInsensitiveDict[str]]:
        raise NotImplementedError()

    def get(
        self, endpoint: str, headers: dict
    ) -> Tuple[int, dict, CaseInsensitiveDict[str]]:
        raise NotImplementedError()

    def patch(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, CaseInsensitiveDict[str]]:
        raise NotImplementedError()

    def delete(self, endpoint: str, headers: dict) -> None:
        raise NotImplementedError()


class SessionClient(HTTPClientProtocol):
    def __init__(self, host: str, bearer_token: str):
        self.bearer_token = bearer_token
        self.host = host

    def post(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, CaseInsensitiveDict[str]]:
        with self._build_session(headers) as s:
            result = s.post(endpoint, json=data)
        if result.status_code != 200:
            raise ValueError(
                f"Request to: {self.host}{endpoint} has returned with status code: {result.status_code}. "
                f'Error: "{str(result.content)}"'
            )

        response_body: Dict = result.json()

        return result.status_code, response_body, result.headers

    def get(
        self, endpoint: str, headers: dict
    ) -> Tuple[int, dict, CaseInsensitiveDict[str]]:
        with self._build_session(headers) as s:
            result = s.get(endpoint)
        if result.status_code != 200:
            raise ValueError(
                f'Request to: {endpoint} has returned with status code: {result.status_code}. Error: "{str(result.content)}"'
            )

        response_body: Dict = result.json()

        return result.status_code, response_body, result.headers

    def patch(
        self, endpoint: str, headers: dict, data: dict
    ) -> Tuple[int, dict, CaseInsensitiveDict[str]]:
        with self._build_session(headers) as s:
            result = s.patch(endpoint, json=data)
        if result.status_code != 204:
            raise ValueError(
                f"Request to: {self.host}{endpoint} has returned with status code: {result.status_code}. "
                f'Error: "{str(result.content)}"'
            )

        response_body: Dict = result.json()

        return result.status_code, response_body, result.headers

    def delete(self, endpoint: str, headers: dict) -> None:
        with self._build_session(headers) as s:
            result = s.delete(endpoint)
        if result.status_code != 204:
            raise ValueError(
                f"Request to: {self.host}{endpoint} has returned with status code: {result.status_code}. "
                f'Error: "{str(result.content)}"'
            )

    def _build_session(self, headers: dict) -> BaseUrlSession:
        s = BaseUrlSession(self.host)
        s.headers.update(headers)
        s.headers.update({"Authorization": f"Bearer {self.bearer_token}"})
        logger.debug(f"{len(headers) + 1} header(s) added to base session.")
        return s
