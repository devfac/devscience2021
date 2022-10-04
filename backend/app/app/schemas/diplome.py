from ast import Pass
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
class DiplomeBase(BaseModel):
    diplome: Optional[str]
    uuid_journey: Optional[str]
    uuid_mention: Optional[str] 


# Properties to receive via API on creation
class DiplomeCreate(DiplomeBase):
    uuid:Optional[UUID]
    num_carte: str
    diplome: str
    uuid_journey: UUID
    uuid_mention: UUID


# Properties to receive via API on update
class DiplomeUpdate(DiplomeBase):
    diplome: Optional[str]
    uuid_journey: Optional[UUID]
    uuid_mention: Optional[UUID]


class DiplomeInDBBase(DiplomeBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Diplome(DiplomeInDBBase):
    num_carte: Optional[str]


# Additional properties stored in DB
class DiplomeInDB(DiplomeInDBBase):
    Pass