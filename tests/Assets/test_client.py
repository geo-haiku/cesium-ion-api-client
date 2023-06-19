import json
from unittest.mock import AsyncMock

import pytest

from Assets.client import AssetsApiClient
from Assets.dtos import (
    ListAssetsQueryParameters,
    CreateAssetRequest,
    AssetInfoPathParams,
    ModifyAssetInfoPathParams,
    ModifyAssetInfoRequest,
    DeleteAssetPathParams,
    AccessTilesPathParams,
    AssetEndpoints,
    ExternalAssetEndpoints,
)
from Assets.enums import AssetType, AssetStatus
from exceptions import MalformedResponseError


@pytest.mark.asyncio
async def test_list_assets_while_link_header_is_present() -> None:
    with open("./fixtures/list_response.json") as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {"Link": "test; aaaa'next'"})

    client = AssetsApiClient(http_client)
    path_parameters = ListAssetsQueryParameters()

    result, res_headers = await client.list_assets(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets?limit=1000&page=1&sortBy=ID&sortOrder=ASC", headers={}
    )

    assert res_headers.next == "es"
    assert res_headers.prev is None

    assert len(result.items) == 2
    first_item = result.items[0]
    assert first_item.id == "1"
    assert first_item.type == AssetType.TERRAIN
    assert first_item.name == "Cesium World Terrain"
    assert (
        first_item.description
        == "High-resolution global terrain tileset curated from several data sources. See the official [Cesium World Terrain](https://cesium.com/content/cesium-world-terrain/) page for details."
    )
    assert first_item.bytes == 0
    assert (
        first_item.attribution
        == "Data available from the U.S. Geological Survey, © CGIAR-CSI, Produced using Copernicus data and information funded by the European Union - EU-DEM layers, Data available from Land Information New Zealand, Data available from data.gov.uk, Data courtesy Geoscience Australia"
    )
    assert first_item.date_added == "2019-04-14T15:25:11.030Z"
    assert first_item.status == AssetStatus.COMPLETE
    assert first_item.percent_complete == 100
    assert first_item.archivable is False
    assert first_item.exportable is False
    second_item = result.items[1]
    assert second_item.id == "92391"
    assert second_item.type == AssetType.THREEDTILES
    assert second_item.name == "My House"
    assert second_item.description == "First attempt at photogrammetry."
    assert second_item.bytes == 28459666
    assert second_item.attribution == ""
    assert second_item.date_added == "2019-04-14T15:28:25.435Z"
    assert second_item.status == AssetStatus.COMPLETE
    assert second_item.percent_complete == 100
    assert second_item.archivable is True
    assert second_item.exportable is True


@pytest.mark.asyncio
async def test_list_assets_while_link_header_is_not_present() -> None:
    with open("./fixtures/list_response.json") as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {"faulty-Link": "test; aaaa'next'"})

    client = AssetsApiClient(http_client)
    path_parameters = ListAssetsQueryParameters()

    result, link_headers = await client.list_assets(path_parameters)
    assert link_headers is None


@pytest.mark.asyncio
async def test_create_a_new_asset() -> None:
    with open("./fixtures/create_response.json") as f:
        res = json.load(f)

    with open("./fixtures/create_request.json") as f:
        req = json.load(f)

    http_client = AsyncMock()
    http_client.post.return_value = (200, res, {})

    req_dto = CreateAssetRequest.parse_obj(req)
    client = AssetsApiClient(http_client)

    result = await client.create_a_new_asset(req_dto)

    http_client.post.assert_called_once_with(
        endpoint="/v1/assets",
        headers={"Content-type": "application/json"},
        data=req_dto.dict(),
    )

    assert result.asset_metadata.id == "21111"
    assert result.asset_metadata.type == AssetType.THREEDTILES
    assert result.asset_metadata.name == "Reichstag"
    assert result.asset_metadata.description == "Example Asset"
    assert result.asset_metadata.attribution == ""
    assert result.asset_metadata.bytes == 0
    assert result.asset_metadata.date_added == "2019-04-19T00:30:54.111Z"
    assert result.asset_metadata.status == AssetStatus.AWAITING_FILES
    assert result.asset_metadata.percent_complete == 0
    assert result.asset_metadata.archivable is False
    assert result.asset_metadata.exportable is True

    assert result.upload_location.endpoint == "https://s3.us-east-1.amazonaws.com"
    assert result.upload_location.bucket == "assets.cesium.com"
    assert result.upload_location.prefix == "sources/21111/"
    assert result.upload_location.access_key == "ASIATXRQLSFCKKLAIVXW"
    assert (
        result.upload_location.secret_access_key
        == "Hd3ZC9yq78hoCR4KYF4atHEnytfgLJMNV0KPdpz8"
    )
    assert (
        result.upload_location.session_token
        == "FQoGZXIvYXdzEIr//////////wEaDIEDvhx6N7x4Rd4+wiKtAht78S1zVze89DICpOxfnl/7kn7ox75U5hCv+UHlynJcbN5N7roU7iOz0SLbp9RrTrXPlUP0agskLV/5DUKcDId9FnZknDLVW03ajCeJMlzQK7vcxXK359OHp9l6OwLofVkkXH5Pd78vNcLEzqkLytoMRA0BK4wM2bFJySbfo89oUSxpwHXgslmlZtwHYOcVIyEQX1DmtNVi7Jsx6btgaqt+taLScYCWFsOrK+mpJX8vhe9NTd3gXiQ2BG01L9spfYP9iwt8eyjq9UAD9HCaQZrYvhK9JKAwBD81dkpkxpg2PL68d5B+yRBt90NgLgJc31raArGvurz9IAf034znL0IZntK56sKLcIYKEg0OzpybP0a4IqSLtHQDAYlHe7Z66ogDWmRMxLW+g4yiGtwovq3k5QU="
    )

    assert result.on_complete.method == "POST"
    assert (
        result.on_complete.url
        == "https://api.cesium.com/v1/assets/21111/uploadComplete"
    )
    assert result.on_complete.fields == {}


@pytest.mark.asyncio
async def test_get_info_about_asset() -> None:
    with open("./fixtures/get_response.json") as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    path_params = AssetInfoPathParams(assetId=123)
    client = AssetsApiClient(http_client)

    result = await client.get_info_about_asset(path_params)

    http_client.get.assert_called_once_with(endpoint="/v1/assets/123", headers={})

    assert result.id == "3812"
    assert result.name == "The Earth At Night"
    assert (
        result.description
        == "The Earth at night, also known as [The Black Marble](https://earthobservatory.nasa.gov/Features/NightLights/)."
    )
    assert (
        result.attribution
        == "[NASA](https://earthobservatory.nasa.gov/image-use-policy)"
    )
    assert result.type == AssetType.THREEDTILES
    assert result.bytes == 8675309
    assert result.date_added == "2019-03-19T13:17:02.838Z"
    assert result.status == AssetStatus.COMPLETE
    assert result.percent_complete == 100
    assert result.archivable is False
    assert result.exportable is True


@pytest.mark.asyncio
async def test_modify_asset_info() -> None:
    with open("./fixtures/modify_request.json") as f:
        req = json.load(f)

    http_client = AsyncMock()
    http_client.patch.return_value = (200, {}, {})

    path_params = ModifyAssetInfoPathParams(assetId=123)
    client = AssetsApiClient(http_client)

    req_dto = ModifyAssetInfoRequest.parse_obj(req)

    await client.modify_asset_info(path_params, req_dto)

    http_client.patch.assert_called_once_with(
        endpoint="/v1/assets/123",
        headers={"Content-type": "application/json"},
        data=req_dto.dict(),
    )


@pytest.mark.asyncio
async def test_delete_asset() -> None:
    http_client = AsyncMock()
    http_client.delete.return_value = (200, {}, {})

    path_params = DeleteAssetPathParams(assetId=123)
    client = AssetsApiClient(http_client)

    await client.delete_asset(path_params)

    http_client.delete.assert_called_once_with(endpoint="/v1/assets/123", headers={})


@pytest.mark.asyncio
async def test_access_tiles_asset_endpoint() -> None:
    with open("./fixtures/access_response.json") as f:
        res = json.load(f)
    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    path_params = AccessTilesPathParams(assetId=123)
    client = AssetsApiClient(http_client)

    result = await client.access_tiles(path_params)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/123/endpoint", headers={}
    )

    assert type(result) == AssetEndpoints
    assert result.type == AssetType.THREEDTILES
    assert result.url == "https://assets.cesium.com/23912/tileset.json"
    assert (
        result.access_token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMjZmNzU0Yy02ZmVkLTQ4ODktOTUyMC0zMDRlMmNjODdiMzEiLCJpZCI6NDQsImFzc2V0cyI6eyIxIjp7InR5cGUiOiJURVJSQUlOIiwiZXh0ZW5zaW9ucyI6W3RydWUsdHJ1ZSx0cnVlXSwicHVsbEFwYXJ0VGVycmFpbiI6ZmFsc2V9fSwic3JjIjoiOGE2NjVmYmMtZDQzMy00ZmMxLWE3NDgtNjRhYWE3MjFiOTgzIiwiaWF0IjoxNTU0MTI4NTUzLCJleHAiOjE1NTQxMzIxNTN9.CWjqdF1LORmCd7nVbHupXyIjCPOfuSOpXwQoaQU_a94"
    )
    assert len(result.attributions) == 1
    attribute = result.attributions[0]
    assert (
        attribute.html
        == '<span><a href="https://cesium.com" target="_blank"><img alt="Cesium ion" src="http://assets.cesium.com/ion-credit.png"></a></span>'
    )
    assert attribute.collapsible is False


@pytest.mark.asyncio
async def test_access_tiles_external_asset_endpoint() -> None:
    with open("./fixtures/external_access_response.json") as f:
        res = json.load(f)
    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    path_params = AccessTilesPathParams(assetId=123)
    client = AssetsApiClient(http_client)

    result = await client.access_tiles(path_params)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/123/endpoint", headers={}
    )

    assert type(result) == ExternalAssetEndpoints
    assert result.type == AssetType.THREEDTILES
    assert result.external_type == "BING"
    assert len(result.attributions) == 1
    attribute = result.attributions[0]
    assert (
        attribute.html
        == '<span><a href="https://cesium.com" target="_blank"><img alt="Cesium ion" src="http://assets.cesium.com/ion-credit.png"></a></span>'
    )
    assert attribute.collapsible is False


@pytest.mark.asyncio
async def test_access_tiles_when_malformed_response() -> None:
    http_client = AsyncMock()
    http_client.get.return_value = (200, {"test": True}, {})

    path_params = AccessTilesPathParams(assetId=123)
    client = AssetsApiClient(http_client)
    with pytest.raises(
        MalformedResponseError,
        match="Provided response is not matching any of supported schemas: <class 'Assets.dtos.ExternalAssetEndpoints'>, <class 'Assets.dtos.AssetEndpoints'>.",
    ):
        await client.access_tiles(path_params)

    http_client.get.assert_called_once_with(
        endpoint="/v1/assets/123/endpoint", headers={}
    )
