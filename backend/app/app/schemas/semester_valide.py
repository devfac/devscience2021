from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class SemesterValideBase(BaseModel):
    semester: Optional[List[str]] = None


# Properties to receive via API on creation
class SemesterValideCreate(SemesterValideBase):
    uuid: Optional[UUID]
    num_carte: str
    semester: List[str]


# Properties to receive via API on update
class SemesterValideUpdate(SemesterValideBase):
    semester: Optional[List[str]]


class SemesterValideInDBBase(SemesterValideBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class SemesterValide(SemesterValideInDBBase):
    num_carte: Optional[str]


# Additional properties stored in DB
class SemesterValideInDB(SemesterValideInDBBase):
    pass
