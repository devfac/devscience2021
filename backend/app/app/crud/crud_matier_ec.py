import uuid
from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import MetaData, Table

from app.crud.base import CRUDBase
from app.db.session import engine
from app.schemas.matier import MatierECUpdate, MatierECCreate, MatierEC


class CRUDMatierEC(CRUDBase[MatierEC, MatierECCreate, MatierECUpdate]):

    def update_ec(self,schema: str, obj_in: MatierECUpdate, uuid:str) -> Optional[MatierEC]:
        obj_in_data = jsonable_encoder(obj_in)
        update_data  = {}
        for field in obj_in_data:
            if obj_in_data[field]:
                update_data[field]= obj_in_data[field]
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("element_const", metadata,autoload=True)
        up = table.update().values(update_data)
        up = up.where(table.columns.uuid == uuid)
        conn.execute(up)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_by_class(self, schema: str, uuid_journey: str, semester: str) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.semester == semester)
        sel = sel.where(table.c.uuid_journey == uuid_journey)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


    def get_by_value_ue(self,schema: str, value_ue: str, semester:str, uuid_journey:UUID) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value_ue == value_ue)
        sel = sel.where(table.c.semester == semester.upper())
        sel = sel.where(table.c.uuid_journey == uuid_journey)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


    def get_by_value(self,schema: str, value: str, semester:str, uuid_journey:UUID) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("element_const", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value == value)
        sel = sel.where(table.c.semester == semester.upper())
        sel = sel.where(table.c.uuid_journey == uuid_journey)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


    def get_by_uuid(self,schema: str, uuid:str) -> Optional[MatierEC]:
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
        sel = sel.where(table.c.semester == obj_in_data['semester'])
        sel = sel.where(table.c.uuid_journey == obj_in_data['uuid_journey'])
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


    def create_ec(self,schema: str, obj_in: MatierECCreate,value:str,key_unique) -> Optional[List[MatierEC]]:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["uuid"] = str(uuid.uuid4())
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
