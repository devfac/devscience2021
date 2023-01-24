import datetime
from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text

from app.crud.base import CRUDBase
from app.models.historic import Historic
from app.schemas.historic import HistoricCreate
from app.utils import format_date


class CRUDHistoric(CRUDBase[Historic, HistoricCreate, HistoricCreate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Historic]:
        return db.query(Historic).filter(Historic.uuid == uuid).first()

    def get_by_email(self, db: Session, *, email: str,  limit: int, skip: int,college_year: str, title: str = "",
            order: str = "asc", order_by: str = "created_at") -> Optional[List[Historic]]:

        filter_ = [and_(Historic.email == email, or_(Historic.college_year == college_year, Historic.college_year == ""))]
        if title != "" and title != "null":
            filter_.append(Historic.title == title)
        return (
            db.query(Historic)
            .filter(*filter_)
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(
            self, db: Session,  limit: int, skip: int,college_year: str, email: str = "", title: str = "",
            order: str = "asc", order_by: str = "created_at"
    ) -> List[Historic]:
        filter_ = [or_(Historic.college_year == college_year, Historic.college_year == "")]
        if email != "" and email != "null":
            filter_.append(Historic.email == email)
        if title != "" and title != "null":
            filter_.append(Historic.title == title)
        return (
            db.query(Historic)
            .order_by(text(f"{order_by} {order}"))
            .filter(and_(*filter_))
            .offset(skip)
            .limit(limit)
            .all()
        )
    def get_count(
            self, db: Session, college_year: str, email: str = "", title: str = ""
    ) -> List[Historic]:
        filter_ = [or_(Historic.college_year == college_year, Historic.college_year == "")]
        if email != "" and email != "null":
            filter_.append(Historic.email == email)
        if title != "" and title != "null":
            filter_.append(Historic.title == title)
        return (
            db.query(Historic)
            .filter(and_(*filter_))
            .all()
        )

    def create(
        self, db: Session, *, obj_in: HistoricCreate
    ) -> Historic:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Historic(**obj_in_data, created_at=format_date())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

historic = CRUDHistoric(Historic)
