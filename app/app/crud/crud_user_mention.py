from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_mention import UserMention
from app.schemas.user_mention import UserMentionCreate, UserMentionUpdate


class CRUDUserMention(CRUDBase[UserMention, UserMentionCreate, UserMentionUpdate]):

    def get_by_id(self, db: Session, *, user_mention_id: int) -> Optional[UserMention]:
        return db.query(UserMention).filter(UserMention.id == user_mention_id).first()
    
    def get_by_user(self, db: Session, *, id_user: int) -> Optional[List[UserMention]]:
        return db.query(UserMention).filter(UserMention.id_user == id_user).all()

    def get_by_user_and_mention(self, db: Session, *, id_user: int, id_mention: int) -> Optional[List[UserMention]]:
        return db.query(UserMention).filter(
            and_(UserMention.id_user == id_user, UserMention.id_mention == id_mention)).first()


user_mention = CRUDUserMention(UserMention)
