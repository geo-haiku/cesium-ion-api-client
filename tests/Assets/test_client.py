import json
from unittest.mock import AsyncMock

import pytest

from Assets.client import AssetsApiClient
from Assets.dtos import ListAssetsQueryParameters
from Assets.enums import AssetType, AssetStatus


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
