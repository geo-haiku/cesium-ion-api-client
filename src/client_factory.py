from typing import Union

from Archives.client import ArchivesApiClient
from Assets.client import AssetsApiClient
from Exports.client import ExportsApiClient
from Tokens.client import TokensApiClient
from User.client import UserApiClient
from enums import Endpoints
from exceptions import NotSupportedEndpointError
from http_client import AsyncClient


class ClientFactory:
    ENDPOINT_TO_API_CLIENT_MAP = {
        Endpoints.ARCHIVES: ArchivesApiClient,
        Endpoints.ASSETS: AssetsApiClient,
        Endpoints.EXPORTS: ExportsApiClient,
        Endpoints.TOKENS: TokensApiClient,
        Endpoints.USER: UserApiClient,
    }

    def __init__(self, host: str, bearer_token: str):
        self.host = host
        self.bearer_token = bearer_token

    def build(
        self, endpoint: Endpoints
    ) -> Union[
        ArchivesApiClient,
        AssetsApiClient,
        ExportsApiClient,
        TokensApiClient,
        UserApiClient,
    ]:
        http_client = AsyncClient(host=self.host, bearer_token=self.bearer_token)
        try:
            client = self.ENDPOINT_TO_API_CLIENT_MAP[endpoint]
        except KeyError as e:
            raise NotSupportedEndpointError(
                f"Provided endpoint {str(e)} is not supported."
            )
        else:
            return client(http_client=http_client)
