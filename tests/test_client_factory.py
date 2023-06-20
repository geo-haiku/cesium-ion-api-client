import pytest

from Tokens.client import TokensApiClient
from client_factory import ClientFactory
from enums import Endpoints
from exceptions import NotSupportedEndpointError


def test_build_when_success() -> None:
    host = "https://google.com"
    bearer_token = "access_token"

    factory = ClientFactory(host, bearer_token)
    result = factory.build(Endpoints.TOKENS)

    assert type(result) == TokensApiClient
    assert result._http_client.host == host
    assert result._http_client.bearer_token == bearer_token


def test_build_when_not_supported_endpoint() -> None:
    host = "https://google.com"
    bearer_token = "access_token"

    factory = ClientFactory(host, bearer_token)
    with pytest.raises(
        NotSupportedEndpointError, match="Provided endpoint 'test' is not supported."
    ):
        factory.build("test")
