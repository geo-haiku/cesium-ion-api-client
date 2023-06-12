from logging import Logger

from User.dtos import ProfileInfoResponse
from http_client import HTTPClientProtocol


class UserApiClient:
    def __init__(self, http_client: HTTPClientProtocol, log: Logger):
        self._http_client = http_client
        self._log = log

    def get_profile_info(self) -> ProfileInfoResponse:
        endpoint_url = "/v1/me"
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        profile_info_response = ProfileInfoResponse.parse_obj(response_body)
        return profile_info_response
