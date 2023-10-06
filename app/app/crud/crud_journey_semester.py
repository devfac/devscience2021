from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.journey_semester import JourneySemester
from app.schemas.journey_semester import JourneySemesterCreate, JourneySemesterUpdate


class CRUDJourneySemester(CRUDBase[JourneySemester, JourneySemesterCreate, JourneySemesterUpdate]):

    def get_by_id(self, db: Session, *, user_mention_id: int) -> Optional[JourneySemester]:
        return db.query(JourneySemester).filter(JourneySemester.id == user_mention_id).first()

    def get_by_journey(self, db: Session, *, id_journey: int) -> Optional[List[JourneySemester]]:
        return db.query(JourneySemester).filter(JourneySemester.id_journey == id_journey).all()


journey_semester = CRUDJourneySemester(JourneySemester)
