from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models import Validation
from app.models.validation import Validation
from app.schemas.validation import ValidationCreate, ValidationUpdate


class CRUDValidation(CRUDBase[Validation, ValidationCreate, ValidationUpdate]):

    def get_by_id(self, db: Session, *, validation_id: str) -> Optional[Validation]:
        return db.query(Validation).filter(Validation.id == validation_id).first()

    def get_by_num_carte(self, db: Session, *, num_carte: str) -> List[Validation]:
        return db.query(Validation).filter(Validation.num_carte == num_carte).all()

    def get_by_journey(self, db: Session, *, id_journey: str, id_journey_: str) -> List[Validation]:
        return db.query(Validation).filter(or_(Validation.id_journey == id_journey,
                                               Validation.id_journey == id_journey_)).all()

    def get_by_journey_and_semester(self, db: Session, *, semester: str, id_journey: str) -> List[Validation]:
        return db.query(Validation).filter(
            and_(Validation.semester == semester,
                 Validation.id_journey == id_journey)).all()

    def get_by_num_carte_and_semester_and_journey(self, db: Session, *, num_carte: str, semester: str, id_journey: str) \
            -> Optional[Validation]:
        return db.query(Validation).filter(
            and_(Validation.num_carte == num_carte, Validation.semester == semester,
                 Validation.id_journey == id_journey)).first()


validation = CRUDValidation(Validation)
