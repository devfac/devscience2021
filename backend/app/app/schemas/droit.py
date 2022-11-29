from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
from .mention import Mention


class DroitBase(BaseModel):
    level: Optional[str]
    droit: Optional[str]
    year: Optional[str]
    uuid_mention: Optional[UUID]


# Properties to receive via API on creation
class DroitCreate(DroitBase):
    level: str
    droit:str
    year: str
    uuid_mention: UUID


# Properties to receive via API on update
class DroitUpdate(DroitBase):
    level: Optional[str]
    droit: Optional[str]
    year: Optional[str]
    uuid_mention: Optional[UUID]



class DroitInDBBase(DroitBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Droit(DroitInDBBase):
    mention: Optional[Mention]


# Additional properties stored in DB
class DroitInDB(DroitInDBBase):
    pass

