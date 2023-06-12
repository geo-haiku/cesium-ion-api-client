
from logging import Logger
from typing import Tuple, Protocol
from requests_toolbelt.sessions import BaseUrlSession

class HTTPClientProtocol(Protocol):
    def post(self, endpoint: str, headers: dict, data: dict) -> Tuple[int, dict, dict]:
        raise NotImplementedError()

    def get(self, endpoint: str, headers: dict) -> Tuple[int, dict, dict]:
        raise NotImplementedError()

    def patch(self, endpoint: str, headers: dict, data: dict) -> Tuple[int, dict, dict]:
        raise NotImplementedError()

    def delete(self, endpoint: str, headers: dict) -> None:
        raise NotImplementedError()

class SessionClient(HTTPClientProtocol):
    def __init__(self, host: str, log: Logger, bearer_token: str):
        self.bearer_token = bearer_token
        self.host = host
        self.log = log

    def post(self, endpoint: str, headers: dict, data: dict) -> Tuple[int, dict, dict]:
        with self._build_session(headers) as s:
            result = s.post(endpoint, json=data)
        if result.status_code != 200:
            raise ValueError(
                f"Request to: {self.host}{endpoint} has returned with status code: {result.status_code}. "
                f'Error: "{str(result.content)}"'
            )

        return result.status_code, result.json(), result.headers

    def get(self, endpoint: str, headers: dict) -> Tuple[int, dict, dict]:
        with self._build_session(headers) as s:
            result = s.get(endpoint)
        if result.status_code != 200:
            raise ValueError(
                f'Request to: {endpoint} has returned with status code: {result.status_code}. Error: "{str(result.content)}"'
            )

        return result.status_code, result.json(), result.headers

    def patch(self, endpoint: str, headers: dict, data: dict) -> Tuple[int, dict, dict]:
        with self._build_session(headers) as s:
            result = s.patch(endpoint, json=data)
        if result.status_code != 204:
            raise ValueError(
                f"Request to: {self.host}{endpoint} has returned with status code: {result.status_code}. "
                f'Error: "{str(result.content)}"'
            )

        return result.status_code, result.json(), result.headers

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
        s.headers.update({'Authorization': f"Bearer {self.bearer_token}"})
        self.log.debug(f"{len(headers) + 1} header successfully added to base session.")
        return s


