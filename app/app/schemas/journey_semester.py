from typing import Optional, Any, List
from uuid import UUID

from pydantic import BaseModel

from .journey import Journey
from .mention import Mention


# Shared properties
class JourneySemesterBase(BaseModel):
    id_journey: Optional[int]
    semester: Optional[str]


# Properties to receive via API on creation
class JourneySemesterCreate(JourneySemesterBase):
    id_journey: int
    semester: str


# Properties to receive via API on update
class JourneySemesterUpdate(JourneySemesterBase):
    pass


class JourneySemesterInDBBase(JourneySemesterBase):
    id: int
    id_journey: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class JourneySemester(JourneySemesterInDBBase):
    journey: Journey


# Additional properties stored in DB
class JourneySemesterInDB(JourneySemesterInDBBase):
    pass


class ResponseJourneySemester(BaseModel):
    count: int
    data: Optional[List[JourneySemester]]
