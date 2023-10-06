from typing import Any, List, Optional
from pydantic import BaseModel


class ValueUEEC(BaseModel):
    name: str
    title: str
    value: float
    type: str


class InteractionBase(BaseModel):
    s1: Optional[List[ValueUEEC]]
    s2: Optional[List[ValueUEEC]]
    s3: Optional[List[ValueUEEC]]
    s4: Optional[List[ValueUEEC]]
    s5: Optional[List[ValueUEEC]]
    s6: Optional[List[ValueUEEC]]
    s7: Optional[List[ValueUEEC]]
    s8: Optional[List[ValueUEEC]]
    s9: Optional[List[ValueUEEC]]
    s10: Optional[List[ValueUEEC]]


# Properties to receive via API on creation
class InteractionCreate(InteractionBase):
    id_journey: int
    id_year: int


# Properties to receive via API on update
class InteractionUpdate(InteractionBase):
    id_journey: Optional[int]
    id_year: Optional[int]


class InteractionInDBBase(InteractionBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Interaction(InteractionInDBBase):
    pass


# Additional properties stored in DB
class InteractionInDB(InteractionInDBBase):
    pass
