import json
from pathlib import Path
from unittest.mock import AsyncMock

from Archives.client import ArchivesApiClient
from Archives.dtos import (
    ListArchivesPathParams,
    ListArchivesResponse,
    CreateArchivePathParams,
    CreateArchiveRequest,
    GetArchivePathParams,
    DeleteArchivePathParams,
)

import pytest

from Archives.enums import ArchiveStatus


@pytest.mark.asyncio
async def test_list_archive() -> None:
    req_path = Path("./Archives/fixtures/list_response.json")
    with open(req_path.resolve()) as f:
        req = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, req, {})

    client = ArchivesApiClient(http_client)
    path_parameters = ListArchivesPathParams(assetId=213)
    result: ListArchivesResponse = await client.list_archive(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/213/archives", headers={}
    )

    assert len(result.items) == 2
    first_item = result.items[0]
    assert first_item.id == 10
    assert first_item.asset_id == 3812
    assert first_item.format == "ZIP"
    assert first_item.status == ArchiveStatus.COMPLETE
    assert first_item.bytes_archived == 102463

    second_item = result.items[1]
    assert second_item.id == 12
    assert second_item.asset_id == 3812
    assert second_item.format == "ZIP"
    assert second_item.status == ArchiveStatus.IN_PROGRESS
    assert second_item.bytes_archived == 17


@pytest.mark.asyncio
async def test_create_archive() -> None:
    req_path = Path("Archives/fixtures/create_request.json")
    with open(req_path.resolve()) as f:
        req = json.load(f)

    res_path = Path("Archives/fixtures/create_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.post.return_value = (200, res, {})

    client = ArchivesApiClient(http_client)
    path_parameters = CreateArchivePathParams(assetId=213)
    body = CreateArchiveRequest.parse_obj(req)
    result = await client.create_archive(path_parameters, body)

    http_client.post.assert_called_once_with(
        endpoint="/v1/assets/213/archives",
        headers={"Content-type": "application/json"},
        data=body,
    )

    assert result.id == 10
    assert result.asset_id == 3812
    assert result.format == "ZIP"
    assert result.status == ArchiveStatus.NOT_STARTED
    assert result.bytes_archived == 0


@pytest.mark.asyncio
async def test_get_info_about_archive() -> None:
    res_path = Path("Archives/fixtures/get_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    client = ArchivesApiClient(http_client)
    path_parameters = GetArchivePathParams(assetId=213, archiveId=321)
    result = await client.get_info_about_archive(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/213/archives/321", headers={}
    )

    assert result.id == 10
    assert result.asset_id == 3812
    assert result.format == "ZIP"
    assert result.status == ArchiveStatus.COMPLETE
    assert result.bytes_archived == 1024


@pytest.mark.asyncio
async def test_delete_archive() -> None:
    http_client = AsyncMock()

    client = ArchivesApiClient(http_client)
    path_parameters = DeleteArchivePathParams(assetId=213, archiveId=321)
    await client.delete_archive(path_parameters)

    http_client.delete.assert_called_once_with(
        endpoint="/v1/assets/213/archives/321", headers={}
    )
