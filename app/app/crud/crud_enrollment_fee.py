from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import EnrollmentFee
from app.models.enrollment_fee import EnrollmentFee
from sqlalchemy import and_
from app.schemas.enrollment_fee import EnrollmentFeeCreate, EnrollmentFeeUpdate


class CRUDEnrollmentFee(CRUDBase[EnrollmentFee, EnrollmentFeeCreate, EnrollmentFeeUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[EnrollmentFee]:
        return db.query(EnrollmentFee).filter(EnrollmentFee.id == uuid).first()

    def get_by_mention_and_year(self, db: Session, *, id_mention: str, id_year: int) -> \
            List[EnrollmentFee]:
        return db.query(EnrollmentFee).filter(
            and_(EnrollmentFee.id_mention == id_mention, EnrollmentFee.id_year == id_year)).all()

    def get_by_level_and_year_mention(
            self, db: Session, *, level: str, id_year: int, id_mention: str
    ) -> Optional[EnrollmentFee]:
        return db.query(EnrollmentFee).filter(
            and_(EnrollmentFee.level == level, EnrollmentFee.id_year == id_year,
                 EnrollmentFee.id_mention == id_mention)).first()


enrollment_fee = CRUDEnrollmentFee(EnrollmentFee)
