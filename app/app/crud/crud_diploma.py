from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.interaction import Diploma
from app.schemas.diploma import DiplomaCreate, DiplomaUpdate


class CRUDDiploma(CRUDBase[Diploma, DiplomaCreate, DiplomaUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[Diploma]:
        return db.query(Diploma).filter(Diploma.id == uuid).first()

    def get_all(self, db: Session) -> Optional[Diploma]:
        return db.query(Diploma).all()


    def get_by_mention(self, db: Session, id_mention: str, college_year: str, limit: int= 100, skip: int =0) -> Optional[Diploma]:
        return (db.query(Diploma)
            .filter(Diploma.college_year == college_year)
            .all())

    def get_by_num_carte(self, db: Session, *,  num_carte: str) -> Optional[
        Diploma]:
        return (
            db.query(Diploma)
            .filter(Diploma.num_carte == num_carte,
            )
            .first()
        )

    def create(
            self, db: Session, *, obj_in: DiplomaCreate
    ) -> Diploma:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


diploma = CRUDDiploma(Diploma)
