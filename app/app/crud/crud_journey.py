from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.journey import Journey
from app.schemas.journey import JourneyCreate, JourneyUpdate


class CRUDJourney(CRUDBase[Journey, JourneyCreate, JourneyUpdate]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[Journey]:
        return db.query(Journey).filter(Journey.id == id).first()

    def get_by_mention(self, db: Session, *, id_mention: int) -> Optional[List[Journey]]:
        return (
            db.query(Journey)
            .filter(Journey.id_mention == id_mention)
            .all())

    def create(self, db: Session, *, obj_in: JourneyCreate) -> Journey:
        db_obj = Journey(
            title=obj_in.title,
            abbreviation=obj_in.abbreviation,
            id_mention=obj_in.id_mention,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


journey = CRUDJourney(Journey)
