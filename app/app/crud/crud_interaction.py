from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionUpdate, ValueUEEC


class CRUDInteraction(CRUDBase[Interaction, InteractionCreate, InteractionUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[Interaction]:
        return db.query(Interaction).filter(Interaction.id == uuid).first()

    def get_by_journey_and_year(self, db: Session, *, id_journey: UUID, id_year: str) -> Optional[Interaction]:
        return (
            db.query(Interaction)
            .filter(
                and_(
                    Interaction.id_journey == id_journey,
                    Interaction.id_year == id_year
                    )
                )
            .first()
        )

interaction = CRUDInteraction(Interaction)
