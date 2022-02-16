from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
class DroitBase(BaseModel):
    niveau: Optional[str]
    droit: Optional[str]
    annee: Optional[str]
    uuid_mention: Optional[UUID]


# Properties to receive via API on creation
class DroitCreate(DroitBase):
    niveau: str
    droit:str
    annee: str
    uuid_mention: UUID


# Properties to receive via API on update
class DroitUpdate(DroitBase):
    niveau: Optional[str]
    droit: Optional[str]
    annee: Optional[str]
    uuid_mention: Optional[UUID]



class DroitInDBBase(DroitBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Droit(DroitInDBBase):
    pass


# Additional properties stored in DB
class DroitInDB(DroitInDBBase):
    pass

