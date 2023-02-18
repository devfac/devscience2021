from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text

from app.crud.base import CRUDBase
from app.models.permission  import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.utils import format_date


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):

    def get_by_email_and_type(self, db: Session, *, email: str, type_: str) -> Optional[Permission]:
        return db.query(Permission).filter(
            and_(Permission.email == email, Permission.type == type_)).first()

    def create(
            self, db: Session, *, obj_in: PermissionCreate, email_sender: str
    ) -> Permission:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, email_sender=email_sender, created_at=format_date())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


permission = CRUDPermission(Permission)
