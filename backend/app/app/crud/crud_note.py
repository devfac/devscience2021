import json
from os import lchown
from typing import Any, List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table, column, update, insert,select
from app.crud.base import CRUDBase
from app.schemas.matier import MatierECUpdate, MatierECCreate,MatierEC
from app.db.session import engine

class CRUDNote(CRUDBase[MatierEC, MatierECCreate, MatierECUpdate]):

    def check_table_exist(self,schemas:str, semestre:str, parcours:str, session:str) -> bool:
        metadata = MetaData(schema = schemas)
        metadata.reflect(bind=engine)
        for table in metadata.tables:
            table_name = table.replace(f'{schemas}.', '')
            if table_name == f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}":
                return True
        return False

    def check_columns_exist(self,schemas:str, semestre:str, parcours:str, session:str) -> Optional[List[str]]:
        metadata = MetaData(schema=schemas, bind=engine)
        columns = []
        table_ = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        for index, table in enumerate(table_.columns):
            columns.append(str(table).partition(".")[2])
        return columns

    def insert_note(self,schema: str,semestre:str,parcours:str,session:str ,num_carte:str) :
        obj_in_data = jsonable_encoder({num_carte})
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        conn = engine.connect()
        ins = insert(table=table)
        ins = ins.values(obj_in_data)
        conn.execute(ins)
        conn.close()

    def read_all_note(self,schema: str,semestre:str,parcours:str, session:str) :
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def update_note(self,schema: str, semestre:str, parcours:str,session:str ,num_carte:str, ue_in:Any):
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        conn = engine.connect()
        up = update(table=table)
        up = up.values(ue_in)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)


    def read_by_num_carte(self,schema: str, semestre:str, parcours:str,session:str, num_carte:str) -> Any:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


    def update_auto(self,schema: str, semestre:str, parcours:str,session:str ,num_carte:str):
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        table_norm = Table(f"note_{semestre.lower()}_{parcours.lower()}_normal", metadata,autoload=True)
        sel = table_norm.select()
        sel = sel.where(table_norm.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        up = table.update()
        up = up.values(out)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)
        conn.close()


    def read_by_credit(self,schema: str, semestre:str, parcours:str,session:str, credit:int) -> Any:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        sel = table.select()
        sel = sel.where(table.columns.credit < credit)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out
        

    def delete_by_num_carte(self,schema: str, semestre:str, parcours:str, session:str,num_carte:str):
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_carte == {num_carte})
        conn.execute(dele)
        conn.close

    def read_ue_moyenne(self,schema: str, semestre:str, parcours:str, session:str,num_carte:str, obj_in:str) -> Any:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}", metadata,autoload=True)
        sel = table.select()
        sel = sel.where(f"table.columns.{num_carte} == {num_carte}")
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

note = CRUDNote(MatierEC)
