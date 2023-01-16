from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bacc_serie import BaccSerie
from app.schemas.bacc_serie import BaccSerieCreate, BaccSerieUpdate


class CRUDBaccSerie(CRUDBase[BaccSerie, BaccSerieCreate, BaccSerieUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[BaccSerie]:
        return db.query(BaccSerie).filter(BaccSerie.uuid == uuid).first()

    
    def get_by_title(self, db: Session, *, title: str) -> Optional[BaccSerie]:
        return db.query(BaccSerie).filter(BaccSerie.title == title).first()

    def get_by_value(self, db: Session, *, value: str) -> Optional[BaccSerie]:
        return db.query(BaccSerie).filter(BaccSerie.value == value).first()
        
    def create(
        self, db: Session, *, obj_in: BaccSerieCreate, value: str,
    ) -> BaccSerie:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = BaccSerie(**obj_in_data, value=value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


bacc_serie = CRUDBaccSerie(BaccSerie)
