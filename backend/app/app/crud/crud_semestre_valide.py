from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sqlalchemy import MetaData, Table, or_, and_
from app.crud.base import CRUDBase
from app.schemas.semestre_valide import SemestreValideCreate, SemestreValideUpdate, SemestreValide
from app.db.session import engine


class CRUDSemestreValide(CRUDBase[SemestreValide, SemestreValideCreate, SemestreValideUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[SemestreValide]:
        return db.query(SemestreValide).filter(SemestreValide.uuid == uuid).first()

    def get_by_num_carte(self, schema: str, num_carte: str) -> Optional[SemestreValide]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("semestre_valide", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def update_sems(self, schema: str, obj_in: SemestreValideUpdate, num_carte: str) -> Optional[SemestreValide]:
        obj_in_data = jsonable_encoder(obj_in)
        update_data = {}
        for field in obj_in_data:
            if obj_in_data[field]:
                update_data[field] = obj_in_data[field]
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("semestre_valide", metadata, autoload=True)
        up = table.update().values(update_data)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        return out

    def create_sems(
            self, schema: str, obj_in: SemestreValideCreate
    ) -> Optional[SemestreValide]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("semestre_valide", metadata, autoload=True)
        ins = table.insert().values(obj_in_data)
        conn.execute(ins)
        sel = table.select()
        sel = sel.where(table.columns.num_carte == obj_in.num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        return out

    def get_all(
            self, schema: str
    ) -> Optional[List[SemestreValide]]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("semestre_valide", metadata, autoload=True)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_sems(self, schema: str, num_carte: str) -> Optional[List[SemestreValide]]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("semestre_valide", metadata, autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_carte == num_carte)
        conn.execute(dele)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


semetre_valide = CRUDSemestreValide(SemestreValide)
