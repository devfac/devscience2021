from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class SemesterBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class SemesterCreate(SemesterBase):
    title: str


# Properties to receive via API on update
class SemesterUpdate(SemesterBase):
    title: Optional[str] = None


class SemesterInDBBase(SemesterBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Semester(SemesterInDBBase):
    pass


# Additional properties stored in DB
class SemesterInDB(SemesterInDBBase):
    pass
