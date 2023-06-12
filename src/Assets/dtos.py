from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import conlist

from Assets.enums import SortByType, SortOrder, AssetStatus, AssetType, SourceType, HeightReference, \
    GeometryCompression, TextureFormat


### List assets

class ListAssetsQueryParameters(BaseModel):
    limit: int = Field(ge=1, le=1000, default=1000)
    page: int = Field(ge=1, default=1)
    search: Optional[str]
    sortBy: SortByType = SortByType.ID
    sortOrder: SortOrder = SortOrder.ASC
    status: List[AssetStatus] = []
    type: List[AssetType] = []

    def to_query_params(self) -> str:
        query_params = f'?limit={self.limit}&page={self.page}&sortBy={self.sortBy.name}&sortOrder={self.sortOrder.value}'
        if self.search:
            query_params += f'&search={self.search}'

        for status in self.status:
            query_params += f'&status={status.value}'
        for type in self.type:
            query_params += f'&type={type.value}'

        return query_params


class AssetMetadata(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    bytes: Optional[int] = Field(ge=0)
    type: AssetType
    status: Optional[AssetStatus]
    date_added: Optional[str] = Field(alias='dateAdded')
    attribution: Optional[str]
    percent_complete: Optional[int] = Field(ge=0, le=100, alias='percentComplete')
    archivable: Optional[bool]
    exportable: Optional[bool]


class ListAssetsResponse(BaseModel):
    items: List[AssetMetadata]





### Create a new asset
class AssetOptions(BaseModel):
    source_type: SourceType = Field(alias='sourceType')


class RasterImagery(AssetOptions):
    pass


class TerrainDatabase(AssetOptions):
    pass


class GeoJson(AssetOptions):
    pass


class CityGML(AssetOptions):
    geometry_compression: GeometryCompression = Field(default=GeometryCompression.DRACO, alias="geometryCompression")
    disable_colors: bool = Field(default=False, alias="disableColors")
    disable_textures: bool = Field(default=False, alias="disableTextures")
    clamp_to_terrain: bool = Field(default=False, alias="clampToTerrain")
    base_terrain_id: Optional[int] = Field(alias="baseTerrainId")


class KML(AssetOptions):
    geometry_compression: GeometryCompression = Field(default=GeometryCompression.DRACO, alias="geometryCompression")
    base_terrain_id: Optional[int] = Field(alias="baseTerrainId")


class ThreeDCapture(AssetOptions):
    position: List[float] = conlist(float, min_items=3, max_items=3)  # [longitude, latitude, height]
    geometry_compression: GeometryCompression = Field(default=GeometryCompression.DRACO, alias="geometryCompression")
    texture_format: TextureFormat = Field(default=TextureFormat.AUTO, alias="textureFormat")


class ThreeDModel(AssetOptions):
    position: List[float] = conlist(float, min_items=3, max_items=3)  # [longitude, latitude, height]
    geometry_compression: GeometryCompression = Field(default=GeometryCompression.DRACO, alias="geometryCompression")
    texture_format: TextureFormat = Field(default=TextureFormat.AUTO, alias="textureFormat")
    optimize: bool = False


class PointCloud(AssetOptions):
    position: List[float] = conlist(float, min_items=3, max_items=3)  # [longitude, latitude, height]
    geometry_compression: GeometryCompression = Field(default=GeometryCompression.DRACO, alias="geometryCompression")


class ThreeDTiles(AssetOptions):
    tileset_json: str = Field(alias="tilesetJson")


class RasterTerrain(AssetOptions):
    height_reference: Optional[HeightReference] = Field(alias="heightReference")
    to_meters: Optional[float] = Field(alias="toMeters")
    base_terrain_id: Optional[int] = Field(alias="baseTerrainId")
    water_mask: Optional[bool] = Field(aliast="waterMask")


class AwsCredentials(BaseModel):
    access_key: Optional[str] = Field(alias="accessKey")
    secret_access_key: Optional[str] = Field(alias="secretAccessKey")


class AssetFrom(BaseModel):
    type: str = 'S3'
    bucket: str
    credentials: AwsCredentials
    keys: List[str] = Field(default=[])
    prefixes: List[str] = Field(default=[])


class CreateAssetRequest(BaseModel):
    name: str
    description: Optional[str]
    attribution: Optional[str]
    type: AssetType
    percent_complete: Optional[int] = Field(ge=0, le=100, alias='percentComplete')
    options: AssetOptions
    asset_from: Optional[AssetFrom] = Field(alias='from')

class UploadLocation(BaseModel):
    endpoint: Optional[str]
    bucket: Optional[str]
    prefix: Optional[str]
    access_key: Optional[str] = Field(alias='accessKey')
    secret_access_key: Optional[str] = Field(alias='secretAccessKey')
    session_token: Optional[str] = Field(alias='sessionToken')


class OnComplete(BaseModel):
    method: Optional[str]
    url: Optional[str]
    fields: Optional[Dict[str, Any]]


class CreateAssetResponse(BaseModel):
    upload_location: Optional[UploadLocation] = Field(alias='uploadLocation')
    on_complete: Optional[OnComplete] = Field(alias='onComplete')
    asset_metadata: Optional[AssetMetadata] = Field(alias='assetMetadata')


### Get info about an asset

class AssetInfoPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')


class AssetInfoResponse(AssetMetadata):
    pass


### Modify asset info

class ModifyAssetInfoPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')


class ModifyAssetInfoRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    attribution: Optional[str]


### Delete an asset
class DeleteAssetPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')


### Access tiles
class AccessTilesPathParams(BaseModel):
    asset_id: int = Field(alias='assetId')


class Attribution(BaseModel):
    html: Optional[str]
    collapsible: Optional[bool]


class AssetEndpoints(BaseModel):
    type: Optional[AssetType]
    url: Optional[str]
    access_token: Optional[str] = Field(alias='accessToken')
    attributions: List[Attribution] = Field([])

class Options(BaseModel):
    url: Optional[str]
    map_style: Optional[str] = Field( alias='mapStyle')
    key: Optional[str]


class ExternalAssetEndpoints(BaseModel):
    external_type: str = Field('BING', alias='externalType')
    type: Optional[AssetType]
    attributions: List[Attribution] = Field([])
    options: Optional[Options]
