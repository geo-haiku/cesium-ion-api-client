from typing import List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class Storage(BaseModel):
    used: Optional[int]
    available: Optional[int]
    total: Optional[int]


class ProfileInfoResponse(BaseModel):
    id: int
    scopes: List[str]
    username: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool] = Field(alias='emailVerified')
    avatar: Optional[str]
    storage: Optional[Storage]
