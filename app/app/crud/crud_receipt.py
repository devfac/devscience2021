from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.student_receipt import StudentReceipt
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate


class CRUDReceipt(CRUDBase[StudentReceipt, ReceiptCreate, ReceiptUpdate]):

    def get_by_id(self, db: Session, *, uuid: str) -> Optional[StudentReceipt]:
        return db.query(StudentReceipt).filter(StudentReceipt.id == uuid).first()

    
    def get_title(self, db: Session, *, title: str) -> Optional[StudentReceipt]:
        return db.query(StudentReceipt).filter(StudentReceipt.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: ReceiptCreate
    ) -> StudentReceipt:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


receipt = CRUDReceipt(StudentReceipt)
