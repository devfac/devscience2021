from typing import List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData,  Table, select, insert, update, delete
from app.crud.base import CRUDBase
from app.schemas.matier import MatierECUpdate, MatierECCreate,MatierEC
from app.db.session import engine


class CRUDMatierEC(CRUDBase[MatierEC, MatierECCreate, MatierECUpdate]):

    def update_ec(self,schema: str, obj_in: MatierECUpdate, uuid:str) -> Optional[MatierEC]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("element_const", metadata,autoload=True)
        up = table.update().values(obj_in_data)
        up = up.where(table.columns.uuid == uuid)
        conn.execute(up)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_by_class(self, schema: str, uuid_parcours: UUID, semestre: str) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.semestre == semestre)
        sel = sel.where(table.c.uuid_parcours == uuid_parcours)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


    def get_by_value_ue(self,schema: str, value_ue: str, semestre:str, uuid_parcours:UUID) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value_ue == value_ue)
        sel = sel.where(table.c.semestre == semestre.upper())
        sel = sel.where(table.c.uuid_parcours == uuid_parcours)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


    def get_by_value(self,schema: str, value: str, semestre:str, uuid_parcours:UUID) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value == value)
        sel = sel.where(table.c.semestre == semestre.upper())
        sel = sel.where(table.c.uuid_parcours == uuid_parcours)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


    def get_by_uuid(self,schema: str, uuid:UUID) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid == uuid)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


    def key_unique(self,schema: str, key_unique:str) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.key_unique == key_unique)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_schema(self,schema: str,obj_in: MatierECCreate, value:str)-> Optional[List[MatierEC]]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value == value)
        sel = sel.where(table.c.semestre == obj_in_data['semestre'])
        sel = sel.where(table.c.uuid_parcours == obj_in_data['uuid_parcours'])
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


    def create_ec(self,schema: str, obj_in: MatierECCreate,value:str,key_unique) -> Optional[List[MatierEC]]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("element_const", metadata,autoload=True)
        ins = table.insert().values(**obj_in_data,value=value,key_unique=key_unique)
        conn.execute(ins)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out


    def get_all(self,schema: str) -> Optional[List[MatierEC]]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("element_const", metadata,autoload=True)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


    def delete_ec(self,schema: str, uuid: str) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"element_const", metadata,autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.uuid == uuid)
        conn.execute(dele)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

matier_ec = CRUDMatierEC(MatierEC)
