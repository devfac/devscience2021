from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

# Shared properties
from .mention import Mention


class ClassroomBase(BaseModel):
    name: Optional[str]
    capacity: Optional[int]


# Properties to receive via API on creation
class ClassroomCreate(ClassroomBase):
    name: str
    capacity: int


# Properties to receive via API on update
class ClassroomUpdate(ClassroomBase):
    name: Optional[str]
    capacity: Optional[int]


class ClassroomInDBBase(ClassroomBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Classroom(ClassroomInDBBase):
    pass


# Additional properties stored in DB
class ClassroomInDB(ClassroomInDBBase):
    pass


class ResponseClassroom(BaseModel):
    count: Optional[int]
    data: Optional[List[Classroom]]
