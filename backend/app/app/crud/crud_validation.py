from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.validation import Validation
from app.schemas.validation import ValidationCreate, ValidationUpdate


class CRUDValidation(CRUDBase[Validation, ValidationCreate, ValidationUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Validation]:
        return db.query(Validation).filter(Validation.uuid == uuid).first()
    
    def get_by_num_carte(self, db: Session, *, num_carte: str) -> Optional[Validation]:
        return db.query(Validation).filter(Validation.num_carte == num_carte).all()


    def get_by_journey(self, db: Session, *, uuid_journey: str) -> Optional[Validation]:
        return db.query(Validation).filter(Validation.uuid_journey == uuid_journey).all()

    def get_by_num_carte_and_semester_and_journey(self, db: Session, *, num_carte: str, semester: str, uuid_journey: str)\
            -> Optional[Validation]:
        return db.query(Validation).filter(
            and_(Validation.num_carte == num_carte, Validation.semester == semester,
                 Validation.uuid_journey == uuid_journey)).first()


validation = CRUDValidation(Validation)
