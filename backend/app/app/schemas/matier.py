from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
class MatiertBase(BaseModel):
    uuid: Optional[UUID]
    title: Optional[str] = None
    value: Optional[str] = None
    semestre: Optional[str] = None
    uuid_parcours: Optional[UUID] = None
    uuid_mention: Optional[UUID] = None

# Properties to receive via API on creation
class MatierUECreate(MatiertBase):
    title: str
    value: str
    credit: int
    semestre: str
    uuid_parcours: UUID
    uuid_mention: UUID

class MatierECCreate(MatiertBase):
    title: str
    value: str
    semestre: str
    value_ue: str
    poids: float
    utilisateur: str
    uuid_parcours: UUID
    uuid_mention: UUID


class MatierUEUpdate(BaseModel):
    uuid: Optional[UUID]
    credit: Optional[int]


class MatierECUpdate(BaseModel):
    uuid: Optional[UUID]
    poids: Optional[float]
    value_ue: Optional[str]
    utilisateur: Optional[str]


class MatierUEInDBBase(MatiertBase):
    credit: Optional[int]

    class Config:
        orm_mode = True

class MatierECInDBBase(MatiertBase):
    poids: Optional[float]
    value_ue: Optional[str]
    utilisateur: Optional[str]

    class Config:
        orm_mode = True


# Additional properties to return via API
class MatierUE(MatierUEInDBBase):
    pass


# Additional properties stored in DB
class MatierUEInDB(MatierUEInDBBase):
    pass

class MatierEC(MatierECInDBBase):
    pass

# Additional properties stored in DB
class MatierECInDB(MatierECInDBBase):
    pass


class MatierUniEc(BaseModel):
    name:Optional[str]
    note:float
    poids: float

class MatierUniUe(BaseModel):
    name:Optional[str]
    note:Optional[float]
    credit: Optional[int]
    ec:Optional[List[MatierUniEc]]

class MatierUni(BaseModel):
    num_carte:Optional[str]
    moyenne:Optional[float]
    ue:Optional[List[MatierUniUe]]


