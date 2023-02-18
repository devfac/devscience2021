import json
from os import lchown
from typing import Any, List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table, column, update, insert, select
from app.crud.base import CRUDBase
from app.schemas.matier import MatierECUpdate, MatierECCreate, MatierEC
from app.db.session import engine


class CRUDSave():

    def insert_data(self, schema: str, table_name: str, obj_in: Any):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(table_name, metadata, autoload=True)
        conn = engine.connect()
        ins = insert(table=table)
        ins = ins.values(obj_in)
        conn.execute(ins)
        conn.close()

    def update_data(self, schema: str, table_name: str, obj_in: Any):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(table_name, metadata, autoload=True)
        conn = engine.connect()
        up = table.update()
        up = up.values(obj_in)
        up = up.where(table.columns.num_carte == obj_in["num_carte"])
        conn.execute(up)
        conn.close()

    def exist_data(self, schema: str, table_name: str, key: str, value: str):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(table_name, metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT * FROM {table} WHERE {key}='{value}'")
        out = result.fetchone()
        conn.close()
        return out

    def read_all_data(self, schema: str, table_name: str) -> List[Any]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(table_name, metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.order_by("num_carte")
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


save = CRUDSave()
