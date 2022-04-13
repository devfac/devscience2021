from typing import List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table
from app.crud.base import CRUDBase
from app.schemas.matier import MatierUEUpdate, MatierUECreate, MatierUE
from app.db.session import engine


class CRUDMatierUE(CRUDBase[MatierUE, MatierUECreate, MatierUEUpdate]):

    def update_ue(self, schema: str, obj_in: MatierUEUpdate, uuid: str) -> Optional[MatierUE]:
        obj_in_data = jsonable_encoder(obj_in)
        update_data = {}
        for field in obj_in_data:
            if obj_in_data[field]:
                update_data[field] = obj_in_data[field]
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"unite_enseing", metadata, autoload=True)
        ins = table.update().values(update_data)
        ins = ins.where(table.columns.uuid == uuid)
        conn.execute(ins)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_by_class(self, schema: str, uuid_parcours: str, semestre: str) -> Optional[List[MatierUE]]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("unite_enseing", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.semestre == semestre.upper())
        sel = sel.where(table.c.uuid_parcours == uuid_parcours)
        sel = sel.order_by(table.columns.title.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_schema(self, schema: str, obj_in: MatierUECreate, value: str) -> Optional[List[MatierUE]]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("unite_enseing", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value == value)
        sel = sel.where(table.c.semestre == obj_in_data['semestre'])
        sel = sel.where(table.c.uuid_parcours == obj_in_data['uuid_parcours'])
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_value(self, schema: str, value: str, semestre: str, uuid_parcours: str) -> Optional[MatierUE]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("unite_enseing", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.c.value == value)
        sel = sel.where(table.c.semestre == semestre)
        sel = sel.where(table.c.uuid_parcours == uuid_parcours)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_uuid(self, schema: str, uuid: str) -> Optional[MatierUE]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("unite_enseing", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid == uuid)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def create_ue(self, schema: str, obj_in: MatierUECreate, value: str, key_unique) -> Optional[MatierUE]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"unite_enseing", metadata, autoload=True)
        ins = table.insert().values(**obj_in_data, value=value, key_unique=key_unique)
        conn.execute(ins)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_all(self, schema: str) -> Optional[MatierUE]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"unite_enseing", metadata, autoload=True)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_ue(self, schema: str, uuid: str) -> Optional[MatierUE]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"unite_enseing", metadata, autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.uuid == uuid)
        conn.execute(dele)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out


matier_ue = CRUDMatierUE(MatierUE)
