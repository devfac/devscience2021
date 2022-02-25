from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import ARRAY


# Shared properties
class ParcoursBase(BaseModel):
    title: Optional[str] = None
    abreviation: Optional[str]
    uuid_mention: Optional[UUID] = None
    semestre: Optional[List[str]]


# Properties to receive via API on creation
class ParcoursCreate(ParcoursBase):
    title: str
    abreviation: str
    uuid_mention: UUID
    semestre: List[str]


# Properties to receive via API on update
class ParcoursUpdate(ParcoursBase):
    title: Optional[str] = None
    abreviation: Optional[str]
    uuid_mention: Optional[UUID]
    semestre: Optional[List[str]]


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
