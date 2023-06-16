import logging

from User.dtos import ProfileInfoResponse
from http_client import HTTPClientProtocol

logger = logging.getLogger(__name__)


class UserApiClient:
    def __init__(self, http_client: HTTPClientProtocol):
        self._http_client = http_client

    async def get_profile_info(self) -> ProfileInfoResponse:
        endpoint_url = "/v1/me"
        status, response_body, headers = await self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        profile_info_response = ProfileInfoResponse.parse_obj(response_body)
        return profile_info_response
