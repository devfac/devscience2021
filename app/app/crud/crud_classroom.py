from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate


class CRUDClassroom(CRUDBase[Classroom, ClassroomCreate, ClassroomUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[Classroom]:
        return db.query(Classroom).filter(Classroom.id == uuid).first()


    def get_by_name(self, db: Session, *, name: str, ) -> Optional[Classroom]:
        return db.query(Classroom).filter(Classroom.name == name).first()

    
    def get_by_capacity(self, db: Session, *, capacity: int) -> Optional[Classroom]:
        return db.query(Classroom).filter(Classroom.capacity == capacity).all()
        
    def create(
        self, db: Session, *, obj_in: ClassroomCreate
    ) -> Classroom:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


classroom = CRUDClassroom(Classroom)

