from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

from .college_year import CollegeYear
from .mention import Mention


class EnrollmentFeeBase(BaseModel):
    level: Optional[str]
    price: Optional[int]
    id_year: Optional[int]
    id_mention: Optional[int]


# Properties to receive via API on creation
class EnrollmentFeeCreate(EnrollmentFeeBase):
    level: str
    price: int
    id_year: int
    id_mention: int


# Properties to receive via API on update
class EnrollmentFeeUpdate(EnrollmentFeeBase):
    pass


class EnrollmentFeeInDBBase(EnrollmentFeeBase):
    id: int
    id_mention: int
    id_year: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnrollmentFee(EnrollmentFeeInDBBase):
    mention: Mention
    year: CollegeYear


# Additional properties stored in DB
class EnrollmentFeeInDB(EnrollmentFeeInDBBase):
    pass


class ResponseEnrollmentFee(BaseModel):
    count: int
    data: Optional[List[EnrollmentFee]]