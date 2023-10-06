from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class BaccSerieBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class BaccSerieCreate(BaccSerieBase):
    title: str


# Properties to receive via API on update
class BaccSerieUpdate(BaccSerieBase):
    title: Optional[str] = None


class BaccSerieInDBBase(BaccSerieBase):
    uuid: Optional[UUID]
    value: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class BaccSerie(BaccSerieInDBBase):
    pass


# Additional properties stored in DB
class BaccSerieInDB(BaccSerieInDBBase):
    pass
