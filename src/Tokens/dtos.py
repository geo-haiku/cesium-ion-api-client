from __future__ import annotations
from typing import Optional, List

from pydantic.fields import Field
from pydantic.main import BaseModel

from Assets.enums import SortOrder
from Tokens.enums import SortByType, TokenScopes

### List tokens

class ListTokensQueryParameters(BaseModel):
    limit: int = Field(ge=1, le=1000, default=1000)
    page: int = Field(ge=1, default=1)
    search: Optional[str]
    sortBy: Optional[SortByType]
    sortOrder: SortOrder = SortOrder.ASC

    def to_query_params(self) -> str:
        query_params = f'?limit={self.limit}&page={self.page}&sortBy={self.sortBy.name}&sortOrder={self.sortOrder.value}'
        if self.search:
            query_params += f'&search={self.search}'

        return query_params


class TokenMetadata(BaseModel):
    id: Optional[str]
    name: Optional[str]
    token: Optional[str]
    date_added: Optional[str] = Field(alias='dateAdded')
    date_modified: Optional[str] = Field(alias='dateModified')
    date_last_used: Optional[str] = Field(alias='dateLastUsed')
    asset_ids: Optional[List[int]] = Field( alias='assetIds')
    is_default: Optional[bool] = Field(alias='isDefault')
    allowed_urls: Optional[List[str]] = Field(alias='allowedUrls')
    scopes: List[TokenScopes]


class ListTokensResponse(BaseModel):
    items: Optional[List[TokenMetadata]]

### Create a new token
class CreateTokenRequest(BaseModel):
    name: Optional[str]
    scopes: List[TokenScopes]
    asset_ids: Optional[List[int]] = Field(alias='assetIds')
    allowed_urls: Optional[List[str]] = Field(alias='allowedUrls')

class CreateTokenResponse(TokenMetadata):
    pass

### Get info about a token

class GetTokenInfoPathParameters(BaseModel):
    token_id: str = Field(alias='tokenId')

class GetTokenInfoResponse(TokenMetadata):
    pass

### Modify token info

class ModifyTokenPathParameters(BaseModel):
    token_id: str = Field(alias='tokenId')

class ModifyTokenRequest(BaseModel):
    name: Optional[str]
    asset_ids: Optional[List[int]] = Field(alias='assetIds')
    scopes: Optional[List[TokenScopes]]
    allowed_urls: Optional[List[str]] = Field(alias='allowedUrls')

### Delete a token
class DeleteTokenPathParameters(BaseModel):
    token_id: str = Field(alias='tokenId')

### Get the default token

class GetDefaultTokenResponse(TokenMetadata):
    pass
