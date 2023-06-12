from typing import Optional, List

from pydantic.fields import Field
from pydantic.main import BaseModel

from Archives.enums import ArchiveStatus


class ArchivePathParams(BaseModel):
    asset_id: int = Field(alias="assetId")
    archive_id: int = Field(alias="archiveId")


### List archives for an asset


class ListArchivesPathParams(BaseModel):
    asset_id: int = Field(alias="assetId")


class ArchiveMetadata(BaseModel):
    id: Optional[int]
    asset_id: Optional[int] = Field(alias="assetId")
    format: Optional[str]
    status: Optional[ArchiveStatus]
    bytes_archived: Optional[int] = Field(alias="bytesArchived", ge=0)


class ListArchivesResponse(BaseModel):
    items: Optional[List[ArchiveMetadata]] = None


### Create an archive


class CreateArchivePathParams(BaseModel):
    asset_id: int = Field(alias="assetId")


class CreateArchiveRequest(BaseModel):
    format: str = "ZIP"


class CreateArchiveResponse(ArchiveMetadata):
    pass


### Get info about an archive


class GetArchivePathParams(ArchivePathParams):
    pass


class GetArchiveResponse(ArchiveMetadata):
    pass


### Delete an archive


class DeleteArchivePathParams(ArchivePathParams):
    pass


### Download an archive


class DownloadArchivePathParams(ArchivePathParams):
    pass
