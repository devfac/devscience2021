from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class SemestreBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class SemestreCreate(SemestreBase):
    title: str


# Properties to receive via API on update
class SemestreUpdate(SemestreBase):
    title: Optional[str] = None


class SemestreInDBBase(SemestreBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Semestre(SemestreInDBBase):
    pass


# Additional properties stored in DB
class SemestreInDB(SemestreInDBBase):
    pass
