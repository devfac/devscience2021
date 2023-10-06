from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.student_years import StudentYears
from app.schemas.student_years import StudentYearsCreate, StudentYearsUpdate


class CRUDStudentYears(CRUDBase[StudentYears, StudentYearsCreate, StudentYearsUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[StudentYears]:
        return db.query(StudentYears).filter(StudentYears.id == uuid).first()

    def get_num_carte_and_year(self, db: Session, *, num_carte: str, id_year: int) -> Optional[StudentYears]:
        return db.query(StudentYears).filter(and_(
            StudentYears.num_carte == num_carte, StudentYears.id_year == id_year)).first()

    def get_num_carte(self, db: Session, *, num_carte: str) -> Optional[StudentYears]:
        return db.query(StudentYears).filter(
            StudentYears.num_carte == num_carte).all()


student_years = CRUDStudentYears(StudentYears)
