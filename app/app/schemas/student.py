from datetime import date
from typing import Optional, List, Any
from uuid import UUID

from pydantic import BaseModel

from app.schemas import Journey, Mention

from .receipt import Receipt

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
    "num_quitance",
    "date_quitance",
    "id_mention",
    "id_journey"
]


class StudentUpdatePhoto(BaseModel):
    photo: Optional[str] = None


# Shared properties
class StudentBase(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[str]
    date_birth: Optional[date] = None
    place_birth: Optional[str] = None
    address: Optional[str] = None
    sex: Optional[str] = None
    nation: Optional[str] = None
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    photo: Optional[str] = None
    id_mention: Optional[int]
    receipt: Optional[Receipt]


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



# Properties to receive via API on creation
class AncienStudentCreate(StudentBase):
    num_carte: str
    last_name: str
    first_name: str
    date_birth: date
    place_birth: str
    address: str
    sex: str
    nation: str
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    mean: float
    baccalaureate_years: str
    type: str
    id_journey: int
    inf_semester: str
    sup_semester: str


class NewStudentCreate(StudentBase):
    num_select: str
    last_name: str
    first_name: Optional[str]
    date_birth: str
    place_birth: str
    address: str
    sex: str
    nation: str
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    type: str
    mean: float
    baccalaureate_num: str
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
    id_mention: int
    id_journey: int


class NewStudentUploaded(StudentBase):
    num_carte: str
    last_name: str
    first_name: Optional[str]
    date_birth: str
    place_birth: str
    address: str
    sex: str
    nation: str
    num_cin: Optional[str] = None
    date_cin: Optional[str] = None
    place_cin: Optional[str] = None
    situation: str
    telephone: Optional[str]
    type: str
    mean: float
    baccalaureate_num: str
    baccalaureate_years: str
    baccalaureate_center: str
    baccalaureate_series: str
    work: str
    receipt_list: Optional[List[str]]
    father_name: Optional[str]
    father_work: Optional[str]
    mother_name: Optional[str]
    mother_work: Optional[str]
    parent_address: Optional[str]
    inf_semester: Optional[str]
    sup_semester: Optional[str]
    id_mention: UUID
    id_journey: UUID


# Properties to receive via API on update
class AncienStudentUpdate(StudentBase):
    mean: Optional[float] = None
    num_carte: Optional[str]
    baccalaureate_years: Optional[str]
    id_mention: Optional[int]
    id_journey: Optional[int]
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
    level: Optional[str]
    id_mention: Optional[int]
    id_journey: Optional[int]
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
    validation: Optional[bool]


# Additional properties stored in DB
class AncienStudentInDB(AncienStudentInDBBase):
    pass


class NewStudent(NewStudentInDBBase):
    enter_year: Optional[str]
    num_carte: Optional[str]
    is_selected: Optional[bool]
    journey: Optional[Journey]
    mention: Optional[Mention]
    receipt: Optional[Receipt]
    situation: Optional[str]
    telephone: Optional[str]


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
