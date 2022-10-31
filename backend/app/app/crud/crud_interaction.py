from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionUpdate, ValueUEEC


class CRUDInteraction(CRUDBase[Interaction, InteractionCreate, InteractionUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Interaction]:
        return db.query(Interaction).filter(Interaction.uuid == uuid).first()

    def get_by_journey_and_year(self, db: Session, *, uuid_journey: UUID, college_year: str) -> Optional[Interaction]:
        return (
            db.query(Interaction)
            .filter(
                and_(
                    Interaction.uuid_journey == uuid_journey,
                    Interaction.college_year == college_year
                    )
                )
            .first()
        )
        
    def create(
        self, db: Session, *, obj_in: InteractionCreate
    ) -> Interaction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

interaction = CRUDInteraction(Interaction)
