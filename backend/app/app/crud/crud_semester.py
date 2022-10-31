from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.semester import Semester
from app.schemas.semester import SemesterCreate, SemesterUpdate


class CRUDSemester(CRUDBase[Semester, SemesterCreate, SemesterUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Semester]:
        return db.query(Semester).filter(Semester.uuid == uuid).first()
        
    def create(
        self, db: Session, *, obj_in: SemesterCreate
    ) -> Semester:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

semester = CRUDSemester(Semester)
