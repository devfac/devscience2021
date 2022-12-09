from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from sqlalchemy import and_, or_
from sqlalchemy import text

from app.models import ConstituentElement
from app.models.matier import TeachingUnit, ConstituentElement
from app.schemas.matier import MatierECCreate, MatierECUpdate, MatierUECreate, MatierUEUpdate


class CRUDTeachingUnit(CRUDBase[TeachingUnit, MatierUECreate, MatierUEUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[TeachingUnit]:
        return db.query(TeachingUnit).filter(TeachingUnit.uuid == uuid).first()


    def get_by_key_unique(self, db: Session, *, key_unique: str) -> Optional[TeachingUnit]:
        return db.query(TeachingUnit).filter(TeachingUnit.key_unique == key_unique).first()

    def get_by_value(self, db: Session, *,value:str ,uuid_journey: UUID, semester: str) -> Optional[TeachingUnit]:
        return (
            db.query(TeachingUnit)
            .filter(and_(TeachingUnit.uuid_journey == uuid_journey,
                         TeachingUnit.semester == semester,
                         TeachingUnit.value == value))
            .order_by(TeachingUnit.title.asc())
            .first())

    def create(
            self, db: Session, *, obj_in: MatierUECreate
    ) -> TeachingUnit:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data,)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
            self, db: Session, limit: int = 100, skip: int = 0,
            order_by: str = "title", order: str = "ASC", uuid_journey: str = "", semester: str = ""
    ) -> List[TeachingUnit]:
        filter_ = []
        if uuid_journey != "" and uuid_journey != "null":
            filter_.append(TeachingUnit.uuid_journey == uuid_journey)
        if semester != "" and semester != "null":
            filter_.append(TeachingUnit.semester == semester)
        return (
            db.query(TeachingUnit)
            .filter(and_(*filter_))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(
            self, db: Session,
    ) -> List[TeachingUnit]:
        return (
            db.query(TeachingUnit)
            .order_by(TeachingUnit.title.asc())
            .all()
        )

    def get_count(
            self, db: Session,  uuid_journey: str = "", semester: str = ""
    ) -> List[TeachingUnit]:
        filter_ = []
        if uuid_journey != "" and uuid_journey != "null":
            filter_.append(TeachingUnit.uuid_journey == uuid_journey)
        if semester != "" and semester != "null":
            filter_.append(TeachingUnit.semester == semester)
        return (
            db.query(self.model)
            .filter(and_(*filter_))
            .all()
        )

    def get_by_class(
            self, db: Session,
            uuid_journey: str,
            semester: str,
    ) -> List[TeachingUnit]:
            return (
                db.query(TeachingUnit)
                .filter(and_(
                    TeachingUnit.uuid_journey == uuid_journey,
                    TeachingUnit.semester == semester,
                ))
                .order_by(TeachingUnit.title.asc())
                .all()
            )


teaching_unit = CRUDTeachingUnit(TeachingUnit)


class CRUDConstituentElement(CRUDBase[ConstituentElement, MatierECCreate, MatierECUpdate]):


    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[ConstituentElement]:
        return db.query(ConstituentElement).filter(ConstituentElement.uuid == uuid).first()


    def get_by_key_unique(self, db: Session, *, key_unique: str) -> Optional[ConstituentElement]:
        return db.query(ConstituentElement).filter(ConstituentElement.key_unique == key_unique).first()

    def get_by_value(self, db: Session, *,value:str ,uuid_journey: UUID, semester: str) -> Optional[ConstituentElement]:
        return (
            db.query(ConstituentElement)
            .filter(and_(ConstituentElement.uuid_journey == uuid_journey,
                         ConstituentElement.semester == semester,
                         ConstituentElement.value == value))
            .order_by(ConstituentElement.title.asc())
            .first())

    def get_by_value_ue(self, db: Session, *,value_ue:str ,uuid_journey: UUID, semester: str) -> Optional[List[ConstituentElement]]:
        return (
            db.query(ConstituentElement)
            .filter(and_(ConstituentElement.uuid_journey == uuid_journey,
                         ConstituentElement.semester == semester,
                         ConstituentElement.value_ue == value_ue))
            .order_by(ConstituentElement.title.asc())
            .all())

    def create(
            self, db: Session, *, obj_in: MatierECCreate
    ) -> ConstituentElement:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data,)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
            self, db: Session,
    ) -> List[ConstituentElement]:
        return (
            db.query(ConstituentElement)
            .order_by(ConstituentElement.title.asc())
            .all()
        )

    def get_multi(
            self, db: Session, limit: int = 100, skip: int = 0,
            order_by: str = "title", order: str = "ASC", uuid_journey: str = "", semester: str = ""
    ) -> List[ConstituentElement]:
        filter_ = []
        if uuid_journey != "" and uuid_journey != "null":
            filter_.append(ConstituentElement.uuid_journey == uuid_journey)
        if semester != "" and semester != "null":
            filter_.append(ConstituentElement.semester == semester)
        return (
            db.query(ConstituentElement)
            .filter(and_(*filter_))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_count(
            self, db: Session,  uuid_journey: str = "", semester: str = ""
    ) -> List[ConstituentElement]:
        filter_ = []
        if uuid_journey != "" and uuid_journey != "null":
            filter_.append(ConstituentElement.uuid_journey == uuid_journey)
        if semester != "" and semester != "null":
            filter_.append(ConstituentElement.semester == semester)
        return (
            db.query(self.model)
            .filter(and_(*filter_))
            .all()
        )

    def get_by_class(
            self, db: Session,
            uuid_journey: str,
            semester: str,
    ) -> List[ConstituentElement]:
        return (
            db.query(ConstituentElement)
            .filter(and_(
                ConstituentElement.uuid_journey == uuid_journey,
                ConstituentElement.semester == semester,
            ))
            .order_by(ConstituentElement.title.asc())
            .all()
        )


constituent_element = CRUDConstituentElement(ConstituentElement)
