from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.base import CRUDBase
from app.models.college_year import CollegeYear
from app.schemas.college_year import CollegeYearCreate, CollegeYearUpdate
from app.utils import create_secret


class CRUDYear(CRUDBase[CollegeYear, CollegeYearCreate, CollegeYearUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[CollegeYear]:
        return db.query(CollegeYear).filter(CollegeYear.id == uuid).first()

    def get_by_title(self, db: Session, title: str) -> Optional[CollegeYear]:
        return db.query(CollegeYear).filter(CollegeYear.title == title).first()


    def get_actual_value(
            self, db: Session,
    ) -> List[CollegeYear]:
        return (
            db.query(self.model)
                .order_by(CollegeYear.title.desc())
                .all()
        )


college_year = CRUDYear(CollegeYear)
