from typing import Optional, Any

from uuid import UUID
from pydantic import BaseModel


# Shared properties
class MentionBase(BaseModel):
    title: Optional[str] = None
    abbreviation: Optional[str] = None
    plugged: Optional[str] = None
    last_num_carte: Optional[int]


# Properties to receive via API on creation
class MentionCreate(MentionBase):
    title: str
    abbreviation: str
    plugged: str
    last_num_carte: int


# Properties to receive via API on update
class MentionUpdate(MentionBase):
    title: Optional[str] = None
    abbreviation: Optional[str] = None
    plugged: Optional[str] = None
    last_num_carte: Optional[int]


class MentionInDBBase(MentionBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Mention(MentionInDBBase):
    value:str


# Additional properties stored in DB
class MentionInDB(MentionInDBBase):
    pass
