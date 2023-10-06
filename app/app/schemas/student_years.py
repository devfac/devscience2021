from typing import Optional, Any, List
from uuid import UUID

from pydantic import BaseModel

from .mention import Mention


# Shared properties
class StudentYearsBase(BaseModel):
    num_carte: Optional[str]
    id_year: Optional[int]


# Properties to receive via API on creation
class StudentYearsCreate(StudentYearsBase):
    num_carte: str
    id_year: int


# Properties to receive via API on update
class StudentYearsUpdate(StudentYearsBase):
    pass


class StudentYearsInDBBase(StudentYearsBase):
    id: int
    num_carte: str
    id_year: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class StudentYears(StudentYearsInDBBase):
    pass


# Additional properties stored in DB
class StudentYearsInDB(StudentYearsInDBBase):
    pass


class ResponseStudentYears(BaseModel):
    count: int
    data: Optional[List[StudentYears]]
