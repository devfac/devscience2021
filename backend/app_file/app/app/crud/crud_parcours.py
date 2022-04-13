from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.parcours import Parcours
from app.schemas.parcours import ParcoursCreate, ParcoursUpdate


class CRUDParcours(CRUDBase[Parcours, ParcoursCreate, ParcoursUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Parcours]:
        return db.query(Parcours).filter(Parcours.uuid == uuid).first()

    def get_by_mention(self, db: Session, *, uuid_mention: UUID) -> Optional[List[Parcours]]:
        return (
            db.query(Parcours)
            .filter(Parcours.uuid_mention == uuid_mention)
            .all())
        
    def create(
        self, db: Session, *, obj_in: ParcoursCreate
    ) -> Parcours:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session
    ) -> List[Parcours]:
        return (
            db.query(self.model)
            .all()
        )


parcours = CRUDParcours(Parcours)
