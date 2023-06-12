from enum import Enum


class SortByType(Enum):
    NAME = 'name'
    LAST_USED = 'last_used'


class TokenScopes(Enum):
    ASSETS_LIST = "assets:list"
    ASSETS_READ = "assets:read"
    ASSETS_WRITE = "assets:write"
    GEOCODE = "geocode"
    PROFILE_READ = "profile:read"
    TOKENS_READ = "tokens:read"
    TOKENS_WRITE = "tokens:write"