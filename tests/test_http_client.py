from dataclasses import dataclass
from typing import Dict
from unittest.mock import MagicMock, patch

import pytest

from exceptions import InvalidCredentials, UnknownError
from http_client import AsyncClient


@dataclass
class MockedReturnValue:
    headers: Dict
    status: int
    content: str

    async def json(self):
        return {"test-body": True}


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.post")
async def test_post(client_session_mock_post: MagicMock) -> None:
    client_session_mock_post.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 200, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    status, res, headers = await client.post(
        "/test", {"Content-type": "application/json"}, {"test": True}
    )

    client_session_mock_post.assert_called_once_with("/test", json={"test": True})
    assert status == 200
    assert res == {"test-body": True}
    assert headers == {"test": True}


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.post")
async def test_post_while_known_error(client_session_mock_post: MagicMock) -> None:
    client_session_mock_post.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 401, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        InvalidCredentials,
        match='POST request to: https://google.com/test has returned with status code: 401. Error: "test"',
    ):
        await client.post("/test", {"Content-type": "application/json"}, {"test": True})

    client_session_mock_post.assert_called_once_with("/test", json={"test": True})


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.post")
async def test_post_while_unknown_error(client_session_mock_post: MagicMock) -> None:
    client_session_mock_post.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 500, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        UnknownError,
        match='POST request to: https://google.com/test has returned with status code: 500. Error: "test"',
    ):
        await client.post("/test", {"Content-type": "application/json"}, {"test": True})

    client_session_mock_post.assert_called_once_with("/test", json={"test": True})


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.get")
async def test_get(client_session_mock_get: MagicMock) -> None:
    client_session_mock_get.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 200, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    status, res, headers = await client.get(
        "/test", {"Content-type": "application/json"}
    )

    client_session_mock_get.assert_called_once_with("/test")
    assert status == 200
    assert res == {"test-body": True}
    assert headers == {"test": True}


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.get")
async def test_get_while_known_error(client_session_mock_get: MagicMock) -> None:
    client_session_mock_get.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 401, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        InvalidCredentials,
        match='GET request to: https://google.com/test has returned with status code: 401. Error: "test"',
    ):
        await client.get("/test", {})

    client_session_mock_get.assert_called_once_with("/test")


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.get")
async def test_get_while_unknown_error(client_session_mock_get: MagicMock) -> None:
    client_session_mock_get.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 500, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        UnknownError,
        match='GET request to: https://google.com/test has returned with status code: 500. Error: "test"',
    ):
        await client.get("/test", {})

    client_session_mock_get.assert_called_once_with("/test")


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.patch")
async def test_patch(client_session_mock_patch: MagicMock) -> None:
    client_session_mock_patch.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 204, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    status, res, headers = await client.patch(
        "/test", {"Content-type": "application/json"}, {"test": True}
    )

    client_session_mock_patch.assert_called_once_with("/test", json={"test": True})
    assert status == 204
    assert res == {"test-body": True}
    assert headers == {"test": True}


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.patch")
async def test_patch_while_known_error(client_session_mock_patch: MagicMock) -> None:
    client_session_mock_patch.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 401, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        InvalidCredentials,
        match='PATCH request to: https://google.com/test has returned with status code: 401. Error: "test"',
    ):
        await client.patch(
            "/test", {"Content-type": "application/json"}, {"test": True}
        )

    client_session_mock_patch.assert_called_once_with("/test", json={"test": True})


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.patch")
async def test_patch_while_unknown_error(client_session_mock_patch: MagicMock) -> None:
    client_session_mock_patch.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 500, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        UnknownError,
        match='PATCH request to: https://google.com/test has returned with status code: 500. Error: "test"',
    ):
        await client.patch(
            "/test", {"Content-type": "application/json"}, {"test": True}
        )

    client_session_mock_patch.assert_called_once_with("/test", json={"test": True})


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.delete")
async def test_delete(client_session_mock_delete: MagicMock) -> None:
    client_session_mock_delete.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 204, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    await client.delete("/test", {"Content-type": "application/json"})

    client_session_mock_delete.assert_called_once_with("/test")


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.delete")
async def test_delete_while_known_error(client_session_mock_delete: MagicMock) -> None:
    client_session_mock_delete.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 401, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        InvalidCredentials,
        match='DELETE request to: https://google.com/test has returned with status code: 401. Error: "test"',
    ):
        await client.delete("/test", {"Content-type": "application/json"})

    client_session_mock_delete.assert_called_once_with("/test")


@pytest.mark.asyncio
@patch("http_client.aiohttp.ClientSession.delete")
async def test_delete_while_unknown_error(
    client_session_mock_delete: MagicMock,
) -> None:
    client_session_mock_delete.return_value.__aenter__.return_value = MockedReturnValue(
        {"test": True}, 500, "test"
    )
    client = AsyncClient("https://google.com", "test-token")

    with pytest.raises(
        UnknownError,
        match='DELETE request to: https://google.com/test has returned with status code: 500. Error: "test"',
    ):
        await client.delete("/test", {"Content-type": "application/json"})

    client_session_mock_delete.assert_called_once_with("/test")
