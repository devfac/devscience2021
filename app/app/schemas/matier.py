from typing import List, Optional
from pydantic import BaseModel
# Shared properties
from .journey import Journey
from .mention import Mention


class Base(BaseModel):
    title: Optional[str] = None
    semester: Optional[str] = None
    id_journey: Optional[int] = None


# Properties to receive via API on creation
class TeachingUnitCreate(Base):
    title: str
    credit: int
    semester: str
    id_journey: int
    value: str
    key_unique: str


class ConstituentElementCreate(Base):
    title: str
    semester: str
    value_ue: str
    weight: float
    teacher: Optional[str]
    is_optional: bool = False
    id_journey: int
    value: str
    key_unique: str


class TeachingUnitUpdate(BaseModel):
    credit: Optional[int]


class ConstituentElementUpdate(BaseModel):
    weight: Optional[float]
    value_ue: Optional[str]
    teacher: Optional[str]
    is_optional: Optional[bool]


class TeachingUnitInDBBase(Base):
    id: int
    credit: Optional[int]
    value: Optional[str]
    id_journey: int
    key_unique: Optional[str]

    class Config:
        orm_mode = True


class ConstituentElementInDBBase(Base):
    id: int
    weight: Optional[float]
    value: Optional[str]
    value_ue: Optional[str]
    is_optional: Optional[bool]
    key_unique: Optional[str]
    teacher: Optional[str]
    id_journey: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class TeachingUnit(TeachingUnitInDBBase):
    journey: Optional[Journey]


# Additional properties stored in DB
class TeachingUnitInDB(TeachingUnitInDBBase):
    pass


class ConstituentElement(ConstituentElementInDBBase):
    journey: Optional[Journey]


# Additional properties stored in DB
class ConstituentElementInDB(ConstituentElementInDBBase):
    pass


class UniEc(BaseModel):
    name: Optional[str]
    note: float
    weight: float


class UniUe(BaseModel):
    name: Optional[str]
    note: Optional[float]
    credit: Optional[int]
    ec: Optional[List[UniEc]]


class Uni(BaseModel):
    num_carte: Optional[str]
    mean: Optional[float]
    ue: Optional[List[UniUe]]


class UEEC(TeachingUnitInDBBase):
    id: Optional[str]
    ec: Optional[List[ConstituentElement]]


class ResponseTeachingUnit(BaseModel):
    count: int
    data: Optional[List[TeachingUnit]]


class ResponseConstituentElement(BaseModel):
    count: int
    data: Optional[List[ConstituentElement]]
