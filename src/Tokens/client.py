import logging
from typing import Tuple, Optional, Dict

from Tokens.dtos import (
    ListTokensQueryParameters,
    ListTokensResponse,
    CreateTokenRequest,
    CreateTokenResponse,
    GetTokenInfoPathParameters,
    GetTokenInfoResponse,
    ModifyTokenRequest,
    ModifyTokenPathParameters,
    DeleteTokenPathParameters,
    GetDefaultTokenResponse,
)
from dtos import PaginationLinks
from http_client import HTTPClientProtocol

logger = logging.getLogger(__name__)


class TokensApiClient:
    def __init__(self, http_client: HTTPClientProtocol):
        self._http_client = http_client

    async def list_tokens(
        self, query_params: ListTokensQueryParameters
    ) -> Tuple[ListTokensResponse, Optional[PaginationLinks]]:
        endpoint_url = "/v2/tokens" + query_params.to_query_params()
        status, response_body, headers = await self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        pagination_links = await self._retrieve_pagination_links(dict(headers))
        list_tokens_response = ListTokensResponse.parse_obj(response_body)
        return list_tokens_response, pagination_links

    async def _retrieve_pagination_links(
        self, headers: Dict
    ) -> Optional[PaginationLinks]:
        try:
            link_header = headers["Link"]
        except KeyError:
            logger.debug("`Link` header is NOT present in the response.`")
            pagination_links = None
        else:
            logger.debug("`Link` header is present in the response.`")
            pagination_links = PaginationLinks.from_header(link_header)
        return pagination_links

    async def create_new_token(
        self, request_body_dto: CreateTokenRequest
    ) -> CreateTokenResponse:
        endpoint_url = "/v2/tokens"
        headers = {"Content-type": "application/json"}
        request_body = request_body_dto.dict()

        status, response_body, headers = await self._http_client.post(
            endpoint=endpoint_url, headers=headers, data=request_body
        )
        create_token_response = CreateTokenResponse.parse_obj(response_body)

        return create_token_response

    async def get_info_about_token(
        self, path_params: GetTokenInfoPathParameters
    ) -> GetTokenInfoResponse:
        endpoint_url = f"/v2/tokens/{path_params.token_id}"
        status, response_body, headers = await self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        info_token_response = GetTokenInfoResponse.parse_obj(response_body)
        return info_token_response

    async def modify_token_info(
        self,
        path_params: ModifyTokenPathParameters,
        request_body_dto: ModifyTokenRequest,
    ) -> None:
        endpoint_url = f"/v2/tokens/{path_params.token_id}"
        request_body = request_body_dto.dict()
        headers = {"Content-type": "application/json"}
        await self._http_client.patch(
            endpoint=endpoint_url, headers=headers, data=request_body
        )

    async def delete_asset(self, path_params: DeleteTokenPathParameters) -> None:
        endpoint_url = f"/v2/tokens/{path_params.token_id}"
        await self._http_client.delete(endpoint=endpoint_url, headers={})

    async def get_default_token(self) -> GetDefaultTokenResponse:
        endpoint_url = "/v2/tokens/default"
        status, response_body, headers = await self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        default_token_response = GetDefaultTokenResponse.parse_obj(response_body)
        return default_token_response
