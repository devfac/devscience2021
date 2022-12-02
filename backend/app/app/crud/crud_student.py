from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from sqlalchemy import and_, or_, text
from app.models.student import Student
from app.schemas.student import AncienStudentCreate, AncienStudentUpdate, NewStudentUpdate, NewStudentCreate


class CRUDAncienStudent(CRUDBase[Student, AncienStudentCreate, AncienStudentUpdate]):

    def get_by_num_carte(self, db: Session, *, num_carte: str) -> Optional[Student]:
        return db.query(Student).filter(Student.num_carte == num_carte).first()

    def get_by_mention(self, db: Session, *, uuid_mention: UUID, limit:int, skip: int,
                       order: str = 'asc', order_by: str = "last_name") -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(and_(Student.uuid_mention == uuid_mention))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def count_by_mention(self, db: Session, *, uuid_mention: UUID, ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(and_(Student.uuid_mention == uuid_mention))
            .all())

    def get_by_class_limit(self,db: Session,
            uuid_journey: str,
            uuid_mention: str,
            semester: str,
            skip: int,
            limit: int,
            order: str = "ASC",
            order_by: str = "last_name"
    ) -> List[Student]:
        if semester.upper() == 'S1':
            return (
                db.query(Student)
                .filter(and_(
                    Student.uuid_mention == uuid_mention,
                    or_(Student.inf_semester == semester.upper(),
                        Student.sup_semester == semester.upper())
                ))
                .order_by(text(f"{order_by} {order}"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            return (
                db.query(Student)
                .filter(and_(
                    Student.uuid_journey == uuid_journey,
                    Student.uuid_mention == uuid_mention,
                    or_(Student.inf_semester == semester.upper(),
                        Student.sup_semester == semester.upper())
                ))
                .order_by(text(f"{order_by} {order}"))
                .offset(skip)
                .limit(limit)
                .all()
            )


    def get_by_sup_semester_and_mention(
            self, db: Session, *, sup_semester: str,
            uuid_mention: UUID, college_year: str,
            limit: int, skip: int, order: str = "asc", order_by:str = "last_name"
    ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(and_(Student.uuid_mention == uuid_mention,
                         Student.sup_semester == sup_semester,
                         Student.actual_years == college_year))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def get_by_jouney(self, db: Session, *, uuid_journey: UUID,
                      college_year: str, limit:int, skip: int,
                      order: str = "asc", order_by: str = "last_name",
                      ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(and_(Student.uuid_mention == uuid_journey, Student.actual_years == college_year))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def create(
            self, db: Session, *, obj_in: AncienStudentCreate
    ) -> Student:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
            self, db: Session, college_year: str, limit: int, skip: int,
            order: str = "asc", order_by: str = "last_name"
    ) -> List[Student]:
        return (
            db.query(Student)
            .filter(and_(
                Student.actual_years == college_year,
                Student.uuid_journey is not None
            ))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_class(
            self, db: Session,
            uuid_journey: str,
            uuid_mention: str,
            semester: str,
            limit: int = 1000,
            skip: int = 0,
            order: str = "asc",
            order_by: str = "last_name",
    ) -> List[Student]:
        if semester.upper() == 'S1':
            return (
                db.query(Student)
                .filter(and_(
                    Student.uuid_mention == uuid_mention,
                    or_(Student.inf_semester == semester.upper(),
                        Student.sup_semester == semester.upper())
                ))
                .order_by(text(f"{order_by} {order}"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            return (
                db.query(Student)
                .filter(and_(
                    Student.uuid_journey == uuid_journey,
                    Student.uuid_mention == uuid_mention,
                    or_(Student.inf_semester == semester.upper(),
                        Student.sup_semester == semester.upper())
                ))
                .order_by(text(f"{order_by} {order}"))
                .offset(skip)
                .limit(limit)
                .all()
            )

    def get_for_stat(self, db: Session, *,
                     uuid_journey: UUID,
                     semester: str,
                     sex: str,
                     type: str,
                     college_year: str,
                     limit: int = 1000,
                     skip: int = 0,
                     order: str = "asc",
                     order_by: str = "last_name"
                     ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(
                and_(Student.uuid_journey == uuid_journey,
                     Student.actual_years == college_year,
                     Student.sup_semester == semester,
                     Student.type == type,
                     Student.sex == sex))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def get_by_sex_for_stat(self, db: Session, *,
                            uuid_journey: UUID,
                            semester: str,
                            sex: str,
                            college_year: str,
                            limit: int = 1000,
                            skip: int = 0
                            ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(
                and_(Student.uuid_journey == uuid_journey,
                     Student.actual_years == college_year,
                     Student.sup_semester == semester,
                     Student.sex == sex))
            .offset(skip)
            .limit(limit)
            .all())

    def get_by_journey_for_stat(self, db: Session, *,
                            uuid_journey: UUID,
                            semester: str,
                            college_year: str,
                            limit: int = 1000,
                            skip: int = 0
                            ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(
                and_(Student.uuid_journey == uuid_journey,
                     Student.actual_years == college_year,
                     Student.sup_semester == semester))
            .offset(skip)
            .limit(limit)
            .all())
    
    def get_by_journey_and_type(self, db: Session, *,
                            uuid_journey: UUID,
                            type_: str,
                            limit: int = 1000,
                            skip: int = 0
                            ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(
                and_(Student.uuid_journey == uuid_journey,
                     Student.type == type_))
            .offset(skip)
            .limit(limit)
            .all())

    def get_by_journey_and_type_and_mean(self, db: Session, *,
                            uuid_journey: UUID,
                            type_: str,
                            mean: float,
                            limit: int = 1000,
                            skip: int = 0
                            ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(
                and_(Student.uuid_journey == uuid_journey,
                     Student.type == type_,
                     Student.mean >= mean))
            .offset(skip)
            .limit(limit)
            .all())

    def remove_carte(self, db: Session, *, num_carte: str) -> Student:
        obj = db.query(Student).filter(Student.num_carte == num_carte).first()
        db.delete(obj)
        db.commit()
        return obj


ancien_student = CRUDAncienStudent(Student)


class CRUDNewStudent(CRUDBase[Student, NewStudentCreate, NewStudentUpdate]):

    def get_by_num_select(self, db: Session, *, num_select: str) -> Optional[Student]:
        return db.query(Student).filter(Student.num_select == num_select).first()

    def get_by_num_carte(self, db: Session, *, num_carte: str) -> Optional[Student]:
        return db.query(Student).filter(Student.num_carte == num_carte).first()

    def get_student_admis(self, db: Session, *,uuid_mention: str, college_year) -> \
            Optional[Student]:
        return(db.query(Student).filter(
                 and_(Student.enter_years == college_year,
                     Student.is_selected == True,
                     Student.num_carte is not None,
                     Student.uuid_mention == uuid_mention,
                     ))
                .all())

    def get_by_mention(self, db: Session, *, uuid_mention: UUID,
                       college_year: str, limit: int=1000, skip: int=0,
                       order: str = "asc", order_by: str = "last_name",
                       ) -> Optional[List[Student]]:
        return (
            db.query(Student).filter(
                and_(Student.uuid_mention == uuid_mention,
                     Student.enter_years == college_year
                     ))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def count_by_mention(self, db: Session, *, uuid_mention: UUID,
                       college_year: str, ) -> Optional[List[Student]]:
        return (
            db.query(Student).filter(
                and_(Student.uuid_mention == uuid_mention,
                     Student.enter_years == college_year
                     ))
            .all())

    def get_all_admis_by_mention(self, db: Session, *, uuid_mention: UUID,
                                 college_year: str, limit: int=1000, skip: int=0,
                                 order: str = "asc", order_by: str = "last_name"
                                 ) -> Optional[
        List[Student]]:
        return (
            db.query(Student).filter(
                and_(Student.uuid_mention == uuid_mention,
                     Student.enter_years == college_year,
                     Student.is_selected == True
                     ))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def get_by_jouney(self, db: Session, *, uuid_journey: UUID,
                      college_year: str, limit: int=1000, skip: int=0,
                      order: str = "asc", order_by: str = "last_name",
                      ) -> Optional[List[Student]]:
        return (
            db.query(Student)
            .filter(and_(Student.uuid_mention == uuid_journey, Student.enter_years == college_year))
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all())

    def create(
            self, db: Session, *, obj_in: NewStudentCreate
    ) -> Student:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100, college_year: str,
            order: str = "asc", order_by: str = "last_name",
    ) -> List[Student]:
        return (
            db.query(Student)
            .filter(Student.enter_years == college_year)
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def remove_select(self, db: Session, *, num_select: str) -> Student:
        obj = db.query(Student).filter(Student.num_select == num_select).first()
        db.delete(obj)
        db.commit()
        return obj


new_student = CRUDNewStudent(Student)
