from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from sqlalchemy import and_, or_
from sqlalchemy import text

from app.models.matier import TeachingUnit, ConstituentElement
from app.schemas.matier import ConstituentElementCreate, ConstituentElementUpdate, TeachingUnitCreate, \
    TeachingUnitUpdate


class CRUDTeachingUnit(CRUDBase[TeachingUnit, TeachingUnitCreate, TeachingUnitUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[TeachingUnit]:
        return db.query(TeachingUnit).filter(TeachingUnit.id == uuid).first()

    def get_by_key_unique(self, db: Session, *, key_unique: str) -> Optional[TeachingUnit]:
        return db.query(TeachingUnit).filter(TeachingUnit.key_unique == key_unique).first()

    def get_by_value(self, db: Session, *, value: str, id_journey: UUID, semester: str) -> Optional[TeachingUnit]:
        return (
            db.query(TeachingUnit)
            .filter(and_(TeachingUnit.id_journey == id_journey,
                         TeachingUnit.semester == semester,
                         TeachingUnit.value == value))
            .order_by(TeachingUnit.title.asc())
            .first())

    def create(
            self, db: Session, *, obj_in: TeachingUnitCreate
    ) -> TeachingUnit:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
            self, db: Session,
    ) -> List[TeachingUnit]:
        return (
            db.query(TeachingUnit)
            .order_by(TeachingUnit.title.asc())
            .all()
        )

    def get_by_class(
            self, db: Session,
            id_journey: str,
            semester: str,
    ) -> List[TeachingUnit]:
        return (
            db.query(TeachingUnit)
            .filter(and_(
                TeachingUnit.id_journey == id_journey,
                TeachingUnit.semester == semester,
            ))
            .order_by(TeachingUnit.title.asc())
            .all()
        )


teaching_unit = CRUDTeachingUnit(TeachingUnit)


class CRUDConstituentElement(CRUDBase[ConstituentElement, ConstituentElementCreate, ConstituentElementUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[ConstituentElement]:
        return db.query(ConstituentElement).filter(ConstituentElement.id == uuid).first()

    def get_by_key_unique(self, db: Session, *, key_unique: str) -> Optional[ConstituentElement]:
        return db.query(ConstituentElement).filter(ConstituentElement.key_unique == key_unique).first()

    def get_by_value(self, db: Session, *, value: str, id_journey: UUID, semester: str) -> Optional[ConstituentElement]:
        return (
            db.query(ConstituentElement)
            .filter(and_(ConstituentElement.id_journey == id_journey,
                         ConstituentElement.semester == semester,
                         ConstituentElement.value == value))
            .order_by(ConstituentElement.title.asc())
            .first())

    def get_by_value_ue(self, db: Session, *, value_ue: str, id_journey: UUID, semester: str) -> Optional[
        List[ConstituentElement]]:
        return (
            db.query(ConstituentElement)
            .filter(and_(ConstituentElement.id_journey == id_journey,
                         ConstituentElement.semester == semester,
                         ConstituentElement.value_ue == value_ue))
            .order_by(ConstituentElement.title.asc())
            .all())

    def get_by_class(
            self, db: Session,
            id_journey: str,
            semester: str,
    ) -> List[ConstituentElement]:
        return (
            db.query(ConstituentElement)
            .filter(and_(
                ConstituentElement.id_journey == id_journey,
                ConstituentElement.semester == semester,
            ))
            .order_by(ConstituentElement.title.asc())
            .all()
        )


constituent_element = CRUDConstituentElement(ConstituentElement)
