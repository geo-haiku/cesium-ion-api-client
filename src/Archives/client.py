import logging
from typing import Dict

from Archives.dtos import (
    ListArchivesPathParams,
    ListArchivesResponse,
    CreateArchivePathParams,
    CreateArchiveRequest,
    CreateArchiveResponse,
    GetArchivePathParams,
    GetArchiveResponse,
    DeleteArchivePathParams,
    DownloadArchivePathParams,
)
from http_client import HTTPClientProtocol

logger = logging.getLogger(__name__)


class ArchivesApiClient:
    def __init__(self, http_client: HTTPClientProtocol):
        self._http_client = http_client

    def list_archive(self, path_params: ListArchivesPathParams) -> ListArchivesResponse:
        endpoint_url = f"/v1/assets/{path_params.asset_id}/archives"
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        list_archives_response = ListArchivesResponse.parse_obj(response_body)
        return list_archives_response

    def create_archive(
        self,
        path_params: CreateArchivePathParams,
        request_body_dto: CreateArchiveRequest,
    ) -> CreateArchiveResponse:
        endpoint_url = f"/v1/assets/{path_params.asset_id}/archives"
        headers = {"Content-type": "application/json"}
        request_body = request_body_dto.dict()

        status, response_body, headers = self._http_client.post(
            endpoint=endpoint_url, headers=headers, data=request_body
        )
        create_archive_response = CreateArchiveResponse.parse_obj(response_body)
        return create_archive_response

    def get_info_about_archive(
        self, path_params: GetArchivePathParams
    ) -> GetArchiveResponse:
        endpoint_url = (
            f"/v1/assets/{path_params.asset_id}/archives/{path_params.archive_id}"
        )
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        get_info_response = GetArchiveResponse.parse_obj(response_body)
        return get_info_response

    def delete_archive(self, path_params: DeleteArchivePathParams) -> None:
        endpoint_url = (
            f"/v1/assets/{path_params.asset_id}/archives/{path_params.archive_id}"
        )
        self._http_client.delete(endpoint=endpoint_url, headers={})

    # TODO: handle downloaded object
    def download_archive(self, path_params: DownloadArchivePathParams) -> Dict:
        endpoint_url = f"/v1/assets/{path_params.asset_id}/archives/{path_params.archive_id}/download"  # noqa: F501
        status, response_body, headers = self._http_client.get(
            endpoint=endpoint_url, headers={}
        )
        return response_body
