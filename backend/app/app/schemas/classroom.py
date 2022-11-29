from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
from .mention import Mention


class ClassroomBase(BaseModel):
    name: Optional[str]
    capacity: Optional[str]


# Properties to receive via API on creation
class ClassroomCreate(ClassroomBase):
    name: str
    capacity:str


# Properties to receive via API on update
class ClassroomUpdate(ClassroomBase):
    name: Optional[str]
    capacity: Optional[str]



class ClassroomInDBBase(ClassroomBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Classroom(ClassroomInDBBase):
    pass


# Additional properties stored in DB
class ClassroomInDB(ClassroomInDBBase):
    pass

