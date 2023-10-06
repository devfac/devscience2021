import datetime
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text

from app.crud.base import CRUDBase
from app.models.invitation  import Invitation
from app.schemas.invitation import InvitationCreate, InvitationUpdate


class CRUDInvitation(CRUDBase[Invitation, InvitationCreate, InvitationUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[List[Invitation]]:
        return (
            db.query(Invitation)
            .filter(Invitation.email == email)
            .order_by(Invitation.created_at.desc())
            .all())

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[Invitation]:
        return db.query(Invitation).filter(Invitation.id == uuid).first()

    def create(
            self, db: Session, *, obj_in: InvitationCreate
    ) -> Invitation:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_at=datetime.datetime.now())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


invitation = CRUDInvitation(Invitation)
