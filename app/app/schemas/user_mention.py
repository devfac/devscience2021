from typing import Optional, Any, List
from uuid import UUID

from pydantic import BaseModel

from .mention import Mention


# Shared properties
class UserMentionBase(BaseModel):
    id_user: Optional[int]
    id_mention: Optional[int]


# Properties to receive via API on creation
class UserMentionCreate(UserMentionBase):
    id_user: int
    id_mention: int


# Properties to receive via API on update
class UserMentionUpdate(UserMentionBase):
    pass


class UserMentionInDBBase(UserMentionBase):
    id: int
    id_user: int
    id_mention: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserMention(UserMentionInDBBase):
    mention: Optional[Mention]


# Additional properties stored in DB
class UserMentionInDB(UserMentionInDBBase):
    pass


class ResponseUserMention(BaseModel):
    count: int
    data: Optional[List[UserMention]]
