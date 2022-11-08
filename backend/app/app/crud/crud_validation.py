from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.interaction import Validation
from app.schemas.validation import ValidationCreate, ValidationUpdate


class CRUDValidation(CRUDBase[Validation, ValidationCreate, ValidationUpdate]):
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Validation]:
        return db.query(Validation).filter(Validation.uuid == uuid).first()

    def get_by_num_carte(self, db: Session, *, num_carte: str) -> Optional[Validation]:
        return db.query(Validation).filter(Validation.num_carte == num_carte).first()

    def create(
            self, db: Session, *, obj_in: ValidationCreate
    ) -> Validation:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
            self, db: Session,
    ) -> List[Validation]:
        return (
            db.query(self.model)
            .all()
        )

validation = CRUDValidation(Validation)
