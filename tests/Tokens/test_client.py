import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from Tokens.client import TokensApiClient
from Tokens.dtos import (
    ListTokensQueryParameters,
    CreateTokenRequest,
    GetTokenInfoPathParameters,
    ModifyTokenPathParameters,
    ModifyTokenRequest,
    DeleteTokenPathParameters,
)
from Tokens.enums import TokenScopes


@pytest.mark.asyncio
async def test_list_archive() -> None:
    res_path = Path("Tokens/fixtures/list_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {"Link": "test; aaaa'next'"})

    client = TokensApiClient(http_client)
    path_parameters = ListTokensQueryParameters()
    result, link_header = await client.list_tokens(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v2/tokens?limit=1000&page=1&sortOrder=ASC", headers={}
    )

    assert link_header.next == "es"
    assert link_header.prev is None

    assert len(result.items) == 2
    first_item = result.items[0]
    assert first_item.id == "58d917ab-f5df-494c-9109-66be3c53219d"
    assert first_item.name == "An Access Token"
    assert (
        first_item.token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1OGQ5MTdhYi1mNWRmLTQ5NGMtOTEwOS02NmJlM2M1MzIxOWQiLCJpZCI6MiwiaWF0IjoxNjM0NTcyNTQzfQ.Cf055OJ96fdxw5NIBT0-JwD4aD9HjYQt9bf6CpadOGM"
    )
    assert first_item.is_default is False
    assert first_item.date_last_used == "2021-10-18T15:55:43.977Z"
    assert first_item.date_added == "2021-09-10T18:29:57.583Z"
    assert first_item.date_modified == "2021-09-11T18:29:57.583Z"
    assert first_item.scopes == [
        TokenScopes.ASSETS_LIST,
        TokenScopes.ASSETS_READ,
        TokenScopes.ASSETS_WRITE,
        TokenScopes.GEOCODE,
        TokenScopes.PROFILE_READ,
    ]
    assert first_item.asset_ids == []

    second_item = result.items[1]
    assert second_item.id == "8494d9bc-a0c7-46ac-b0f5-58bdd6a9724a"
    assert second_item.name == "Another New Token"
    assert (
        second_item.token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4NDk0ZDliYy1hMGM3LTQ2YWMtYjBmNS01OGJkZDZhOTcyNGEiLCJpZCI6MiwiaWF0IjoxNjMzOTgyNjk5fQ.JcD0nmNbO-vVQsoa5w8CudbsCeuN1d7Svmy_GzoehHg"
    )
    assert second_item.is_default is False
    assert second_item.date_last_used == "2021-10-11T20:04:59.380Z"
    assert second_item.date_added == "2021-09-09T18:29:57.583Z"
    assert second_item.date_modified == "2021-09-10T18:29:57.583Z"
    assert second_item.scopes == [TokenScopes.ASSETS_READ, TokenScopes.GEOCODE]
    assert second_item.asset_ids == [80, 98]


@pytest.mark.asyncio
async def test_list_archive_while_link_header_is_faulty() -> None:
    res_path = Path("Tokens/fixtures/list_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {"faulty-Link": "test; aaaa'next'"})

    client = TokensApiClient(http_client)
    path_parameters = ListTokensQueryParameters()
    result, link_header = await client.list_tokens(path_parameters)

    http_client.get.assert_called_once_with(
        endpoint="/v2/tokens?limit=1000&page=1&sortOrder=ASC", headers={}
    )
    assert link_header is None


@pytest.mark.asyncio
async def test_create_new_token() -> None:
    res_path = Path("Tokens/fixtures/create_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    req_path = Path("Tokens/fixtures/create_request.json")
    with open(req_path.resolve()) as f:
        req = json.load(f)

    http_client = AsyncMock()
    http_client.post.return_value = (200, res, {})
    req_dto = CreateTokenRequest.parse_obj(req)

    client = TokensApiClient(http_client)
    result = await client.create_new_token(req_dto)

    http_client.post.assert_called_once_with(
        endpoint="/v2/tokens",
        headers={"Content-type": "application/json"},
        data=req_dto.dict(),
    )

    assert result.id == "3171672f-b6a3-43ae-90d5-0d559a7bf73b"
    assert result.name == "Token"
    assert (
        result.token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMTcxNjcyZi1iNmEzLTQzYWUtOTBkNS0wZDU1OWE3YmY3M2IiLCJpZCI6MSwiaWF0IjoxNjM0Njc1OTU0fQ.cRbNs2IKXbvZjVpjWIId3YB3CeppiIQgbR7mZTKC1UI"
    )
    assert result.is_default is False
    assert result.date_last_used == "2021-10-19T20:39:14.372Z"
    assert result.date_added == "2021-10-19T20:39:14.372Z"
    assert result.date_modified == "2021-10-19T20:39:14.372Z"
    assert result.scopes == [
        TokenScopes.ASSETS_READ,
        TokenScopes.GEOCODE,
        TokenScopes.PROFILE_READ,
    ]
    assert result.asset_ids == [98, 96, 94, 89]


@pytest.mark.asyncio
async def test_get_info_about_token() -> None:
    res_path = Path("Tokens/fixtures/get_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})
    path_parameters = GetTokenInfoPathParameters(tokenId=123)

    client = TokensApiClient(http_client)
    result = await client.get_info_about_token(path_parameters)

    http_client.get.assert_called_once_with(endpoint="/v2/tokens/123", headers={})

    assert result.id == "a4538dc7-f583-4d9e-889e-35e2db4de534"
    assert result.name == "New Token"
    assert (
        result.token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1OGQ5MTdhYi1mNWRmLTQ5NGMtTEwOS02NmJlM2M1MzIxOWQiLCJpZCI6MiwiaWF0IjoxNjM0NTcyNTQzfQ.Cf055OJ6fdxw5NIBT0-JwD4aD9HjYQt9bf6CpadOGM"
    )
    assert result.is_default is False
    assert result.date_last_used == "2019-03-19T13:17:02.838Z"
    assert result.date_added == "2019-03-19T13:17:02.838Z"
    assert result.date_modified == "2019-03-19T13:17:02.838Z"
    assert result.scopes == [TokenScopes.PROFILE_READ]
    assert result.asset_ids == [90, 98, 99, 100]
    assert result.allowed_urls == [
        "https://example.com",
        "https://subdomain.example.com",
        "https://example.com/path/",
        "https://example.com:8080",
    ]


@pytest.mark.asyncio
async def test_modify_token_info() -> None:
    req_path = Path("Tokens/fixtures/modiy_request.json")
    with open(req_path.resolve()) as f:
        req = json.load(f)

    http_client = AsyncMock()

    path_parameters = ModifyTokenPathParameters(tokenId=123)
    request_dto = ModifyTokenRequest.parse_obj(req)
    client = TokensApiClient(http_client)
    await client.modify_token_info(path_parameters, request_dto)

    http_client.patch.assert_called_once_with(
        endpoint="/v2/tokens/123",
        headers={"Content-type": "application/json"},
        data=request_dto.dict(),
    )


@pytest.mark.asyncio
async def test_delete_asset() -> None:
    http_client = AsyncMock()

    path_parameters = DeleteTokenPathParameters(tokenId=123)
    client = TokensApiClient(http_client)
    await client.delete_asset(path_parameters)

    http_client.delete.assert_called_once_with(endpoint="/v2/tokens/123", headers={})


@pytest.mark.asyncio
async def test_get_default_token() -> None:
    res_path = Path("Tokens/fixtures/get_default_response.json")
    with open(res_path.resolve()) as f:
        res = json.load(f)

    http_client = AsyncMock()
    http_client.get.return_value = (200, res, {})

    client = TokensApiClient(http_client)
    result = await client.get_default_token()

    http_client.get.assert_called_once_with(endpoint="/v2/tokens/default", headers={})

    assert result.id == "a4538dc7-f583-4d9e-889e-35e2db4de534"
    assert result.name == "New Token"
    assert (
        result.token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1OGQ5MTdhYi1mNWRmLTQ5NGMtTEwOS02NmJlM2M1MzIxOWQiLCJpZCI6MiwiaWF0IjoxNjM0NTcyNTQzfQ.Cf055OJ6fdxw5NIBT0-JwD4aD9HjYQt9bf6CpadOGM"
    )
    assert result.is_default is True
    assert result.date_last_used == "2019-03-19T13:17:02.838Z"
    assert result.date_added == "2019-03-19T13:17:02.838Z"
    assert result.date_modified == "2019-03-19T13:17:02.838Z"
    assert result.scopes == [TokenScopes.PROFILE_READ]
    assert result.asset_ids == [90, 98, 99, 100]
