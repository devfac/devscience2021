from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.semestre_valide import SemestreValide
from app.schemas.semestre_valide import SemestreValideCreate, SemestreValideUpdate


class CRUDSemestreValide(CRUDBase[SemestreValide, SemestreValideCreate, SemestreValideUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[SemestreValide]:
        return db.query(SemestreValide).filter(SemestreValide.uuid == uuid).first()

    
    def get_by_num_carte(self, db: Session, *, num_carte: str) -> Optional[SemestreValide]:
        return db.query(SemestreValide).filter(SemestreValide.num_carte == num_carte).first()
        
    def create(
        self, db: Session, *, obj_in: SemestreValideCreate
    ) -> SemestreValide:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[SemestreValide]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )


semetre_valide = CRUDSemestreValide(SemestreValide)
