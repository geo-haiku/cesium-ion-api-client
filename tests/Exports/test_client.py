import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from Exports.client import ExportsApiClient
from Exports.dtos import (
    ListExportsPathParams,
    ExportAssetRequest,
    ExportAssetPathParams,
    GetExportStatusPathParams,
)
from Exports.enums import ExportsStatus


@pytest.mark.asyncio
async def test_list_assets_while_link_header_is_present() -> None:
    res_path = Path("Exports/fixtures/list_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {"Link": "test; aaaa'next'"})

    client = ExportsApiClient(http_client)
    path_parameters = ListExportsPathParams(assetId=123)

    result, res_headers = await client.list_exports(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/123/exports", headers={}
    )

    assert res_headers.next == "es"
    assert res_headers.prev is None

    assert len(result.items) == 2
    first_item = result.items[0]
    assert first_item.id == "1"
    assert first_item.asset_id == 3812
    assert first_item.date_added == "2022-09-16T04:06:48.897Z"
    assert first_item.status == ExportsStatus.COMPLETE
    assert first_item.bytes_exported == 762347342
    assert first_item.to.type == "S3"
    assert first_item.to.bucket == "myBucket"
    assert first_item.to.prefix == "/"
    second_item = result.items[1]
    assert second_item.id == "1"
    assert second_item.asset_id == 3812
    assert second_item.date_added == "2022-09-16T04:06:48.897Z"
    assert second_item.status == ExportsStatus.ERROR
    assert second_item.bytes_exported == 0
    assert second_item.to.type == "S3"
    assert second_item.to.bucket == "ion-exports"
    assert second_item.to.prefix == "/3812"


@pytest.mark.asyncio
async def test_list_assets_while_link_header_is_not_present() -> None:
    res_path = Path("Exports/fixtures/list_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {"faulty-Link": "test; aaaa'next'"})

    client = ExportsApiClient(http_client)
    path_parameters = ListExportsPathParams(assetId=123)

    result, link_headers = await client.list_exports(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/123/exports", headers={}
    )

    assert link_headers is None


@pytest.mark.asyncio
async def test_export_asset() -> None:
    res_path = Path("Exports/fixtures/export_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    req_path = Path("Exports/fixtures/export_request.json")
    with open(req_path.resolve()) as f:
        req = json.load(f)

    http_client = AsyncMock()
    http_client.post.return_value = (200, res, {})
    req_dto = ExportAssetRequest.parse_obj(req)

    client = ExportsApiClient(http_client)
    path_parameters = ExportAssetPathParams(assetId=123)

    result = await client.export_asset(path_parameters, req_dto)

    http_client.post.assert_called_once_with(
        endpoint="/v1/assets/123/exports",
        headers={"Content-type": "application/json"},
        data=req_dto.dict(),
    )

    assert result.id == "1"
    assert result.asset_id == 3812
    assert result.status == ExportsStatus.NOT_STARTED
    assert result.bytes_exported == 0
    assert result.to.type == "S3"
    assert result.to.bucket == "myBucket"
    assert result.to.prefix == "/"


@pytest.mark.asyncio
async def test_get_export_asset() -> None:
    res_path = Path("Exports/fixtures/get_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    client = ExportsApiClient(http_client)
    path_parameters = GetExportStatusPathParams(assetId=123, exportId=321)

    result = await client.get_export_status(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/123/exports/321", headers={}
    )

    assert result.id == "1"
    assert result.asset_id == 3812
    assert result.status == ExportsStatus.COMPLETE
    assert result.bytes_exported == 1024
    assert result.date_added == "2022-09-20T16:16:02.838Z"
    assert result.to.type == "S3"
    assert result.to.bucket == "string"
    assert result.to.prefix == "string"
