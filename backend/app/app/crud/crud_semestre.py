from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.semestre import Semestre
from app.schemas.semestre import SemestreCreate, SemestreUpdate


class CRUDSemestre(CRUDBase[Semestre, SemestreCreate, SemestreUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Semestre]:
        return db.query(Semestre).filter(Semestre.uuid == uuid).first()
        
    def create(
        self, db: Session, *, obj_in: SemestreCreate
    ) -> Semestre:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Semestre]:
        return (
            db.query(self.model)
            .all()
        )


semetre = CRUDSemestre(Semestre)
