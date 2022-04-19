from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sqlalchemy import MetaData, Table, or_, and_
from app.crud.base import CRUDBase
from app.schemas.diplome import DiplomeCreate, DiplomeUpdate, Diplome
from app.db.session import engine


class CRUDDiplome(CRUDBase[Diplome, DiplomeCreate, DiplomeUpdate]):

    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Diplome]:
        return db.query(Diplome).filter(Diplome.uuid == uuid).first()

    
    def get_by_num_carte(self, schema:str, num_carte: str) -> Optional[Diplome]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("diplome", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_mention(self, schema:str, uuid_mention: str) -> Optional[Diplome]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("diplome", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_mention == uuid_mention)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def update_diplome(self, schema:str, obj_in: DiplomeUpdate, num_carte:str) -> Optional[List[Diplome]]:
        obj_in_data = jsonable_encoder(obj_in) 
        update_data  = {}
        for field in obj_in_data:
            if obj_in_data[field]:
                update_data[field]= obj_in_data[field]
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("diplome", metadata,autoload=True)
        up = table.update().values(update_data)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out
        
    def create_diplome(
        self, schema:str, obj_in: DiplomeCreate
    ) -> Optional[List[Diplome]]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("diplome", metadata,autoload=True)
        ins = table.insert().values(obj_in_data)
        conn.execute(ins)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_all(
        self, schema:str
    ) -> Optional[List[Diplome]]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("diplome", metadata,autoload=True)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_diplome(self,schema: str, num_carte: str) -> Optional[List[Diplome]]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("diplome", metadata,autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_carte == num_carte)
        conn.execute(dele)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


diplome = CRUDDiplome(Diplome)
