from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class CollegeYearBase(BaseModel):
    title: Optional[str] = None
    mean: Optional[float]


# Properties to receive via API on creation
class CollegeYearCreate(CollegeYearBase):
    title: str
    mean: float


# Properties to receive via API on update
class CollegeYearUpdate(BaseModel):
    mean: Optional[float]


class CollegeYearInDBBase(CollegeYearBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class CollegeYear(CollegeYearInDBBase):
    code: Optional[str] = None


# Additional properties stored in DB
class CollegeYearInDB(CollegeYearInDBBase):
    pass
