from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
# Shared properties
from .journey import Journey
from .mention import Mention


class MatiertBase(BaseModel):
    title: Optional[str] = None
    semester: Optional[str] = None
    uuid_journey: Optional[UUID] = None


# Properties to receive via API on creation
class MatierUECreate(MatiertBase):
    title: str
    credit: int
    semester: str
    uuid_journey: UUID
    value: str
    key_unique: str


class MatierECCreate(MatiertBase):
    title: str
    semester: str
    value_ue: str
    weight: float
    teacher: Optional[str]
    is_optional: bool = False
    uuid_journey: UUID
    value: str
    key_unique: str


class MatierUEUpdate(BaseModel):
    credit: Optional[int]


class MatierECUpdate(BaseModel):
    weight: Optional[float]
    value_ue: Optional[str]
    teacher: Optional[str]
    is_optional: Optional[bool]


class MatierUEInDBBase(MatiertBase):
    credit: Optional[int]
    value: Optional[str]
    key_unique: Optional[str]

    class Config:
        orm_mode = True


class MatierECInDBBase(MatiertBase):
    weight: Optional[float]
    value: Optional[str]
    value_ue: Optional[str]
    is_optional: Optional[bool]
    key_unique: Optional[str]
    teacher: Optional[str]

    class Config:
        orm_mode = True


# Additional properties to return via API
class MatierUE(MatierUEInDBBase):
    uuid: Optional[str]
    journey: Optional[Journey]
    abbreviation_journey: Optional[str]

# Additional properties stored in DB
class MatierUEInDB(MatierUEInDBBase):
    pass


class MatierEC(MatierECInDBBase):
    uuid: Optional[str]
    journey: Optional[Journey]
    abbreviation_journey: Optional[str]


# Additional properties stored in DB
class MatierECInDB(MatierECInDBBase):
    pass


class MatierUniEc(BaseModel):
    name: Optional[str]
    note: float
    weight: float


class MatierUniUe(BaseModel):
    name: Optional[str]
    note: Optional[float]
    credit: Optional[int]
    ec: Optional[List[MatierUniEc]]


class MatierUni(BaseModel):
    num_carte: Optional[str]
    moyenne: Optional[float]
    ue: Optional[List[MatierUniUe]]


class MatierUEEC(MatierUEInDBBase):
    uuid: Optional[str]
    ec:Optional[List[MatierEC]]

