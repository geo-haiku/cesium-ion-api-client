import json
from unittest.mock import AsyncMock

import pytest

from User.client import UserApiClient


@pytest.mark.asyncio
async def test_profile_info() -> None:
    with open("./fixtures/get_response.json") as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    client = UserApiClient(http_client)

    result = await client.get_profile_info()

    http_client.get.assert_called_once_with(endpoint="/v1/me", headers={})

    assert result.id == 212352
    assert result.scopes == ["assets:read", "profile:read"]
    assert result.username == "mamato"
    assert result.email == "matt@cesium.com"
    assert result.email_verified is True
    assert (
        result.avatar
        == "https://www.gravatar.com/avatar/4f14cc6c584f41d89ef1d34c8986ebfb.jpg?d=mp"
    )
    assert result.storage.used == 214526475
    assert result.storage.available == 53472564725
    assert result.storage.total == 53687091200
