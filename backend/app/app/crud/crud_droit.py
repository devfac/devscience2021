from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.droit import Droit
from sqlalchemy import and_
from app.schemas.droit import DroitCreate, DroitUpdate


class CRUDDroit(CRUDBase[Droit, DroitCreate, DroitUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Droit]:
        return db.query(Droit).filter(Droit.uuid == uuid).first()


    def get_by_mention_and_year(self, db: Session, *, uuid_mention: str, year: str) -> Optional[Droit]:
        return db.query(Droit).filter(and_(Droit.uuid_mention == uuid_mention, Droit.year == year)).all()

    
    def get_by_level_and_year(self, db: Session, *, level: str, year:str, uuid_mention:str) -> Optional[Droit]:
        return db.query(Droit).filter( and_(Droit.level == level, Droit.year == year, Droit.uuid_mention == uuid_mention)).first()
        
    def create(
        self, db: Session, *, obj_in: DroitCreate
    ) -> Droit:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session
    ) -> List[Droit]:
        return (
            db.query(self.model)
            .all()
        )


droit = CRUDDroit(Droit)

