import logging
from typing import Tuple, Optional, Dict, Union

from Assets.dtos import (
    ListAssetsQueryParameters,
    ListAssetsResponse,
    CreateAssetRequest,
    CreateAssetResponse,
    AssetInfoPathParams,
    AssetInfoResponse,
    ModifyAssetInfoPathParams,
    ModifyAssetInfoRequest,
    DeleteAssetPathParams,
    AccessTilesPathParams,
    AssetEndpoints,
    ExternalAssetEndpoints,
)
from dtos import PaginationLinks
from exceptions import MalformedResponseError
from http_client import HTTPClientProtocol

logger = logging.getLogger(__name__)


class AssetsApiClient:
    def __init__(self, http_client: HTTPClientProtocol):
        self._http_client = http_client

    def list_assets(
        self, query_params: ListAssetsQueryParameters
    ) -> Tuple[ListAssetsResponse, Optional[PaginationLinks]]:
        endpoint_url = "/v1/assets" + query_params.to_query_params()
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        pagination_links = self._retrieve_pagination_links(dict(headers))
        list_assets_response = ListAssetsResponse.parse_obj(response_body)
        return list_assets_response, pagination_links

    def _retrieve_pagination_links(self, headers: Dict) -> Optional[PaginationLinks]:
        try:
            link_header = headers["Link"]
        except KeyError:
            logging.debug("`Link` header is NOT present in the response.`")
            pagination_links = None
        else:
            logging.debug("`Link` header is present in the response.`")
            pagination_links = PaginationLinks.from_header(link_header)
        return pagination_links

    def create_a_new_asset(
        self, request_body_dto: CreateAssetRequest
    ) -> CreateAssetResponse:
        endpoint_url = "/v1/assets"
        headers = {"Content-type": "application/json"}
        request_body = request_body_dto.dict()

        status, response_body, headers = self._http_client.post(
            endpoint=endpoint_url, headers=headers, data=request_body
        )
        create_asset_response = CreateAssetResponse.parse_obj(response_body)

        return create_asset_response

    def get_info_about_asset(
        self, path_params: AssetInfoPathParams
    ) -> AssetInfoResponse:
        endpoint_url = f"/v1/assets/{path_params.asset_id}"
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        info_asset_response = AssetInfoResponse.parse_obj(response_body)
        return info_asset_response

    def modify_asset_info(
        self,
        path_params: ModifyAssetInfoPathParams,
        request_body_dto: ModifyAssetInfoRequest,
    ) -> None:
        endpoint_url = f"/v1/assets/{path_params.asset_id}"
        request_body = request_body_dto.dict()
        headers = {"Content-type": "application/json"}
        self._http_client.patch(
            endpoint=endpoint_url, headers=headers, data=request_body
        )

    def delete_asset(self, path_params: DeleteAssetPathParams) -> None:
        endpoint_url = f"/v1/assets/{path_params.asset_id}"
        self._http_client.delete(endpoint=endpoint_url, headers={})

    def access_tiles(
        self, path_params: AccessTilesPathParams
    ) -> Union[AssetEndpoints, ExternalAssetEndpoints]:
        endpoint_url = f"/v1/assets/{path_params.asset_id}/endpoint"
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        return self._translate_to_proper_endpoint_dto(response_body)

    def _translate_to_proper_endpoint_dto(
        self, response_body: dict
    ) -> Union[AssetEndpoints, ExternalAssetEndpoints]:
        desired_types = [AssetEndpoints, ExternalAssetEndpoints]
        for type in desired_types:
            try:
                endpoint_dto = type.parse_obj(response_body)
            except ValueError as e:
                logging.debug(
                    f"The provided response is not matching the schema of type: `{type}` because of {str(e)}."  # noqa: F501
                )
            else:
                return endpoint_dto
        raise MalformedResponseError(
            f"Provided response is not matching any of supported schemas: {', '.join(str(desired_types))}."
        )
