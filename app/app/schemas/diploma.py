from ast import Pass
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
class DiplomaBase(BaseModel):
    num_carte: Optional[str]
    licence_title: Optional[str]
    master_title: Optional[str] 


# Properties to receive via API on creation
class DiplomaCreate(DiplomaBase):
    num_carte: str


# Properties to receive via API on update
class DiplomaUpdate(DiplomaBase):
    id_journey: Optional[UUID]
    id_mention: Optional[UUID]


class DiplomaInDBBase(DiplomaBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Diploma(DiplomaInDBBase):
    pass


# Additional properties stored in DB
class DiplomaInDB(DiplomaInDBBase):
    pass