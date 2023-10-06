from typing import List, Optional, Any

from pydantic import BaseModel
# Shared properties
from .mention import Mention


class JourneyBase(BaseModel):
    title: Optional[str] = None
    abbreviation: Optional[str]
    id_mention: Optional[int]


# Properties to receive via API on creation
class JourneyCreate(JourneyBase):
    title: str
    abbreviation: str
    id_mention: int
    semester: List[str]


# Properties to receive via API on update
class JourneyUpdate(JourneyBase):
    semester: Optional[List[str]]


class JourneyInDBBase(JourneyBase):
    id: Optional[int]
    id_mention: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Journey(JourneyInDBBase):
    mention: Optional[Mention]
    semester_list: Optional[List[str]]


# Additional properties stored in DB
class JourneyInDB(JourneyInDBBase):
    pass


class ResponseJourney(BaseModel):
    count: int
    data: Optional[List[Journey]]
