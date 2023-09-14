from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel
from .student import AncienStudent
from .mention import Mention
from .journey import Journey


# Shared properties
class ValidationBase(BaseModel):
    semester: Optional[str]
    session: Optional[str]
    year: Optional[str]
    mean: Optional[float]
    credit: Optional[int]
    num_carte: Optional[str]
    uuid_journey: Optional[UUID]


# Properties to receive via API on creation
class ValidationCreate(ValidationBase):
    semester: str
    session: str
    year: str
    mean: str
    credit: str
    num_carte: str
    uuid_journey: UUID


# Properties to receive via API on update
class ValidationUpdate(ValidationBase):
    pass


class ValidationNoteUpdate(BaseModel):
    num_carte: str
    validation: bool


class ValidationInDBBase(ValidationBase):
    uuid: Optional[UUID]
    num_carte: str
    uuid_journey: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Validation(ValidationInDBBase):
    student: Optional[AncienStudent]
    journey: Optional[Journey]


# Additional properties stored in DB
class ValidationInDB(ValidationInDBBase):
    pass
