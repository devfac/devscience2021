from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.college_year import CollegeYear
from app.schemas.college_year import CollegeYearCreate, CollegeYearUpdate
from app.utils import create_secret


class CRUDYear(CRUDBase[CollegeYear, CollegeYearCreate, CollegeYearUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[CollegeYear]:
        return db.query(CollegeYear).filter(CollegeYear.uuid == uuid).first()

    def get_by_title(self, db: Session, title: str) -> Optional[CollegeYear]:
        return db.query(CollegeYear).filter(CollegeYear.title == title).first()

    def create(
            self, db: Session, *, obj_in: CollegeYearCreate
    ) -> CollegeYear:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, code=create_secret())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
            self, db: Session,
    ) -> List[CollegeYear]:
        return (
            db.query(self.model)
                .order_by(CollegeYear.title.desc())
                .all()
        )

    def get_actual_value(
            self, db: Session,
    ) -> List[CollegeYear]:
        return (
            db.query(self.model)
                .order_by(CollegeYear.title.desc())
                .all()
        )


college_year = CRUDYear(CollegeYear)
