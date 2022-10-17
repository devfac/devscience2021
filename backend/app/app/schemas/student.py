from typing import Optional, List, Any
from uuid import UUID

from pydantic import BaseModel

from app.schemas import Journey, Mention

keys = [
    "num_carte",
    "nom",
    "prenom",
    "date_naiss",
    "lieu_naiss",
    "adresse",
    "sexe",
    "nation",
    "num_cin",
    "date_cin",
    "lieu_cin",
    "montant",
    "bacc_anne",
    "etat",
    "photo",
    "num_quitance",
    "date_quitance",
    "uuid_mention",
    "uuid_journey"
]


# Shared properties
class StudentBase(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    date_birth: Optional[str] = None
    place_birth: Optional[str] = None
    address: Optional[str] = None
    sex: Optional[str] = None
    photo: Optional[str] = None
    nation: Optional[str] = None
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    uuid_mention: Optional[UUID]
    actual_years: Optional[str]


class SelectStudentCreate(StudentBase):
    num_select: str
    is_selected: Optional[bool] = False
    enter_years: str
    level: str
    telephone: Optional[str]


class SelectStudentBase(StudentBase):
    num_select: Optional[str]
    is_selected: Optional[bool] = False
    enter_years: Optional[str]
    mention: Optional[Mention]
    level: Optional[str]
    telephone: Optional[str]

    class Config:
        orm_mode = True

class Receipt(BaseModel):
    num: Optional[str]
    date: Optional[str]
    price: Optional[str]
    year: Optional[str]

# Properties to receive via API on creation
class AncienStudentCreate(StudentBase):
    num_carte: str
    last_name: str
    first_name: str
    date_birth: str
    place_birth: str
    address: str
    sex: str
    nation: str
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    receipt: Optional[Receipt]
    receipt_list: List[Optional[Receipt]]
    mean: float
    baccalaureate_years: str
    type: str
    photo: str
    uuid_journey: UUID
    inf_semester: str
    sup_semester: str

class NewStudentCreate(StudentBase):
    num_select: str
    last_name: str
    first_name: str
    date_birth: str
    place_birth: str
    address: str
    sex: str
    nation: str
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    type: str
    photo: str
    receipt: Optional[Receipt]
    receipt_list: List[Optional[Receipt]]
    mean: float
    baccalaureate_years: str
    baccalaureate_center: str
    baccalaureate_series: str
    work: str
    father_name: Optional[str]
    father_work: Optional[str]
    mother_name: Optional[str]
    mother_work: Optional[str]
    parent_address: Optional[str]
    level: str
    uuid_mention: UUID
    uuid_journey: UUID


# Properties to receive via API on update
class AncienStudentUpdate(StudentBase):
    mean: Optional[float] = None
    num_carte: Optional[str]
    baccalaureate_years: Optional[str]
    uuid_mention: Optional[UUID]
    uuid_journey: Optional[UUID]
    inf_semester: Optional[str]
    sup_semester: Optional[str]


class NewStudentUpdate(StudentBase):
    num_select: Optional[str]
    num_carte: Optional[str]
    situation: Optional[str]
    telephone: Optional[str]
    baccalaureate_num: Optional[str]
    baccalaureate_center: Optional[str]
    baccalaureate_years: Optional[str]
    baccalaureate_series: Optional[str]
    work: Optional[str]
    father_name: Optional[str]
    father_work: Optional[str]
    mother_name: Optional[str]
    mother_work: Optional[str]
    parent_address: Optional[str]
    receipt: Optional[Receipt]
    receipt_list: List[Optional[Receipt]]
    level: Optional[str]
    uuid_mention: Optional[UUID]
    uuid_journey: Optional[UUID]
    inf_semester: Optional[str]
    sup_semester: Optional[str]
    is_selected: Optional[bool] = True


class AncienStudentInDBBase(StudentBase):
    num_carte: Optional[str]
    baccalaureate_years: Optional[str]
    type: Optional[str]
    mean: Optional[float] = None
    inf_semester: Optional[str]
    sup_semester: Optional[str]

    class Config:
        orm_mode = True


class NewStudentInDBBase(StudentBase):
    num_select: Optional[str]
    baccalaureate_num: Optional[str]
    baccalaureate_center: Optional[str]
    baccalaureate_years: Optional[str]
    baccalaureate_series: Optional[str]
    work: Optional[str]
    father_name: Optional[str]
    father_work: Optional[str]
    mother_name: Optional[str]
    mother_work: Optional[str]
    parent_address: Optional[str]
    level: Optional[str]

    class Config:
        orm_mode = True


# Additional properties to return via API
class AncienStudent(AncienStudentInDBBase):
    journey: Optional[Journey]
    receipt: Optional[Receipt]


# Additional properties stored in DB
class AncienStudentInDB(AncienStudentInDBBase):
    pass


class NewStudent(NewStudentInDBBase):
    enter_year: Optional[str]
    num_carte: Optional[str]
    is_selected: Optional[bool]
    journey: Optional[Journey]
    receipt: Optional[Receipt]
    situation: Optional[str]
    telephone: Optional[str]
    receipt: Optional[Receipt]

class NewStudentSelect(NewStudentInDBBase):
    enter_year: Optional[str]
    num_select: Optional[str]
    is_selected: Optional[bool]

# Additional properties stored in DB
class NewStudentInDB(NewStudentInDBBase):
    pass


class CarteStudent(BaseModel):
    num_carte: str
    last_name: str
    first_name: str
    date_birth: str
    place_birth: str
    num_cin: Optional[str]
    date_cin: Optional[str]
    place_cin: Optional[str]
    level: str
    journey: str

