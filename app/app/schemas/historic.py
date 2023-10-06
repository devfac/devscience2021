from typing import Optional, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel


# Shared properties
class HistoricBase(BaseModel):
    email: Optional[str]
    action: Optional[str]
    title: Optional[str]
    value: Optional[str]
    id_year: Optional[int]


# Properties to receive via API on creation
class HistoricCreate(HistoricBase):
    email: str
    title: str
    value: str
    action: str


class HistoricInDBBase(HistoricBase):
    uuid: Optional[UUID]
    created_at: date

    class Config:
        orm_mode = True


# Additional properties to return via API
class Historic(HistoricInDBBase):
    pass


# Additional properties stored in DB
class HistoricInDB(HistoricInDBBase):
    pass
