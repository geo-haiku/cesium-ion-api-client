from enum import Enum


class SortByType(Enum):
    ID = "id"
    NAME = "name"
    DESCRIPTION = "description"
    BYTES = "bytes"
    TYPE = "type"
    STATUS = "status"
    DATE_ADDED = "date_added"


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class AssetStatus(Enum):
    AWAITING_FILES = "AWAITING_FILES"
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    DATA_ERROR = "DATA_ERROR"


class AssetType(Enum):
    THREEDTILES = "3DTILES"
    GLTF = "GLTF"
    IMAGERY = "IMAGERY"
    TERRAIN = "TERRAIN"
    KML = "KML"
    CZML = "CZML"
    GEOJSON = "GEOJSON"


class SourceType(Enum):
    RASTER_IMAGERY = "RASTER_IMAGERY"
    RASTER_TERRAIN = "RASTER_TERRAIN"
    TERRAIN_DATABASE = "TERRAIN_DATABASE"
    CITYGML = "CITYGML"
    KML = "KML"
    THREED_CAPTURE = "3D_CAPTURE"
    THREED_MODEl = "3D_MODEL"
    POINT_CLOUD = "POINT_CLOUD"
    THREEDTILES = "3DTILES"
    CZML = "CZML"
    GEOJSON = "GEOJSON"


class HeightReference(Enum):
    MEAN_SEA_LEVEL = "MEAN_SEA_LEVEL"
    WGS84 = "WGS84"


class GeometryCompression(Enum):
    NONE = "NONE"
    DRACO = "DRACO"


class TextureFormat(Enum):
    AUTO = "AUTO"
    WEBP = "WEBP"
