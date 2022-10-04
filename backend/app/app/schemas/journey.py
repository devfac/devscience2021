from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
from .mention import Mention


class JourneyBase(BaseModel):
    title: Optional[str] = None
    abbreviation: Optional[str]
    uuid_mention: Optional[UUID] = None
    semester: Optional[List[str]]


# Properties to receive via API on creation
class JourneyCreate(JourneyBase):
    title: str
    abbreviation: str
    uuid_mention: UUID
    semester: List[str]


# Properties to receive via API on update
class JourneyUpdate(JourneyBase):
    title: Optional[str] = None
    abbreviation: Optional[str]
    uuid_mention: Optional[UUID]
    semester: Optional[List[str]]


class JourneyInDBBase(JourneyBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Journey(JourneyInDBBase):
    mention: Optional[Mention]
    mention_title: Optional[str]


# Additional properties stored in DB
class JourneyInDB(JourneyInDBBase):
    pass
