from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.journey import Journey
from app.schemas.journey import JourneyCreate, JourneyUpdate


class CRUDJourney(CRUDBase[Journey, JourneyCreate, JourneyUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Journey]:
        return db.query(Journey).filter(Journey.uuid == uuid).first()

    def get_by_mention(self, db: Session, *, uuid_mention: UUID) -> Optional[List[Journey]]:
        return (
            db.query(Journey)
            .filter(Journey.uuid_mention == uuid_mention)
            .all())
        
    def create(
        self, db: Session, *, obj_in: JourneyCreate
    ) -> Journey:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

journey = CRUDJourney(Journey)
