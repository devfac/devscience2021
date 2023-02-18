from typing import Any, List, Optional
from uuid import UUID

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
    uuid_journey: UUID
    college_year: str

# Properties to receive via API on update
class InteractionUpdate(InteractionBase):
    uuid_journey: Optional[UUID]
    college_year: Optional[str]

class InteractionInDBBase(InteractionBase):
    uuid: Optional[UUID]

    class Config:
        orm_mode = True

# Additional properties to return via API
class Interaction(InteractionInDBBase):
    pass

# Additional properties stored in DB
class InteractionInDB(InteractionInDBBase):
    pass
