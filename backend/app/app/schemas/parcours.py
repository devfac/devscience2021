from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel

# Shared properties
class ParcoursBase(BaseModel):
    title: Optional[str] = None
    abreviation:Optional[str]
    uuid_mention: Optional[UUID] = None


# Properties to receive via API on creation
class ParcoursCreate(ParcoursBase):
    title: str
    abreviation:str
    uuid_mention: UUID


# Properties to receive via API on update
class ParcoursUpdate(ParcoursBase):
    title: Optional[str] = None
    abreviation:Optional[str]
    uuid_mention: Optional[UUID]


class ParcoursInDBBase(ParcoursBase):
    uuid: Optional[UUID]
    class Config:
        orm_mode = True


# Additional properties to return via API
class Parcours(ParcoursInDBBase):
    pass


# Additional properties stored in DB
class ParcoursInDB(ParcoursInDBBase):
    pass
