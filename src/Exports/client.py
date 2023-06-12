from logging import Logger
from typing import Dict, Optional, Tuple

from Exports.dtos import (
    ListExportsPathParams,
    ListExportsResponse,
    ExportAssetPathParams,
    ExportAssetRequest,
    ExportAssetResponse,
    GetExportStatusPathParams,
    GetExportStatusResponse,
)
from dtos import PaginationLinks
from http_client import HTTPClientProtocol


class ExportsApiClient:
    def __init__(self, http_client: HTTPClientProtocol, log: Logger):
        self._http_client = http_client
        self._log = log

    def list_exports(
        self, path_params: ListExportsPathParams
    ) -> Tuple[ListExportsResponse, Optional[PaginationLinks]]:
        endpoint_url = f"/v1/assets/{path_params.asset_id}/exports"
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        pagination_links = self._retrieve_pagination_links(dict(headers))
        list_exports_response = ListExportsResponse.parse_obj(response_body)
        return list_exports_response, pagination_links

    def _retrieve_pagination_links(self, headers: Dict) -> Optional[PaginationLinks]:
        try:
            link_header = headers["Link"]
        except KeyError:
            self._log.debug("`Link` header is NOT present in the response.`")
            pagination_links = None
        else:
            self._log.debug("`Link` header is present in the response.`")
            pagination_links = PaginationLinks.from_header(link_header)
        return pagination_links

    def export_asset(
        self, path_params: ExportAssetPathParams, request_body_dto: ExportAssetRequest
    ) -> ExportAssetResponse:
        endpoint_url = f"/v1/assets/{path_params.asset_id}/exports"
        headers = {"Content-type": "application/json"}
        request_body = request_body_dto.dict()

        status, response_body, headers = self._http_client.post(
            endpoint=endpoint_url, headers=headers, data=request_body
        )
        export_asset_response = ExportAssetResponse.parse_obj(response_body)
        return export_asset_response

    def get_export_status(
        self, path_params: GetExportStatusPathParams
    ) -> GetExportStatusResponse:
        endpoint_url = (
            f"/v1/assets/{path_params.asset_id}/exports/{path_params.export_id}"
        )
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        get_export_status = GetExportStatusResponse.parse_obj(response_body)
        return get_export_status
