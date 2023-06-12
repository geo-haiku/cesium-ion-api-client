from __future__ import annotations

from typing import List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from Exports.enums import ExportsStatus


### List exports for an asset

class ListExportsPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')

class To(BaseModel):
    type: Optional[str]
    bucket: Optional[str]
    prefix: Optional[str]


class ExportMetadata(BaseModel):
    id: Optional[int]
    asset_id: Optional[int] = Field(alias='assetId')
    date_added: Optional[str] = Field(alias='dateAdded')
    status: Optional[ExportsStatus]
    bytes_exported: Optional[int] = Field(ge=0, alias='bytesExported')
    to: Optional[To]


class ListExportsResponse(BaseModel):
    items: Optional[List[ExportMetadata]] = None

### Export an asset

class ExportAssetPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')

class ExportAssetRequest(BaseModel):
    format: str = 'S3'
    bucket: str
    prefix: str
    access_key_id: str = Field( alias='accessKeyId')
    secret_access_key: str = Field(alias='secretAccessKey')
    session_token: Optional[str] = Field(alias='sessionToken')


class ExportAssetResponse(ExportMetadata):
    pass

### Get the status of an export

class GetExportStatusPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')
    export_id: int = Field(alias='exportId')

class GetExportStatusResponse(ExportMetadata):
    pass