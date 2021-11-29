from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.anne_univ import AnneUniv
from app.schemas.anne_univ import AnneUnivCreate, AnneUnivUpdate
from app.utils import create_secret


class CRUDSemestre(CRUDBase[AnneUniv, AnneUnivCreate, AnneUnivUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[AnneUniv]:
        return db.query(AnneUniv).filter(AnneUniv.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[AnneUniv]:
        return db.query(AnneUniv).filter(AnneUniv.title == title).first()
        
    def create(
        self, db: Session, *, obj_in: AnneUnivCreate
    ) -> AnneUniv:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data,code=create_secret() )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[AnneUniv]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(AnneUniv.title.desc())
            .all()
        )


anne_univ = CRUDSemestre(AnneUniv)
