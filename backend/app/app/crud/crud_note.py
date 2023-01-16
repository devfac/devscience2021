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


class CRUDNote(CRUDBase[MatierEC, MatierECCreate, MatierECUpdate]):

    def check_table_exist( self, semester: str, journey: str, session: str) -> bool:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        for table in metadata.tables:
            table_name = table.replace('.', '')
            if table_name == f"note_{journey.lower()}_{semester.lower()}_{session.lower()}":
                return True
        return False

    def check_columns_exist(self, semester: str, journey: str, session: str) -> Optional[List[str]]:
        metadata = MetaData(bind=engine)
        columns = []
        table_ = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        for index, table in enumerate(table_.columns):
            if str(table).partition(".")[2] != 'num_carte' and str(table).partition(".")[2] != 'mean' \
                    and str(table).partition(".")[2] != 'credit':
                columns.append(str(table).partition(".")[2])
        return columns

    def insert_note(self, semester: str, journey: str, session: str, num_carte: str, year: str):
        obj_in_data = jsonable_encoder({"num_carte":num_carte, "year":year})
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        ins = insert(table=table)
        ins = ins.values(obj_in_data)
        conn.execute(ins)
        conn.close()

    def read_all_note(self, semester: str, journey: str, session: str, year:str, limit: int = 1000, skip: int = 0):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.year == year)
        sel = sel.offset(skip)
        sel = sel.limit(limit)
        sel = sel.order_by(table.columns.num_carte.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def read_all_note_count(self, semester: str, journey: str, session: str, year:str, ):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.year == year)
        sel = sel.order_by(table.columns.num_carte.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def read_note_succes(self, semester: str, journey: str, session: str, value_matier: str):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte, {value_matier} FROM {table} WHERE {value_matier} >= 10 ")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_ue(self,semester: str, journey: str, session: str, list_ue: list, year: str):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte, {list_ue} FROM {table} WHERE year = '{year}'")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_failed(self, semester: str, journey: str, session: str, value_matier: str):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte, {value_matier} FROM {table} WHERE {value_matier} < 10  OR {value_matier} IS NULL ")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean_and_credit_equals(self, schema: str, semester: str, journey: str, session: str,
                                               mean: float, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte,mean,credit FROM {table} WHERE mean >= {mean} and credit = {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean_and_credit_sup(self, schema: str, semester: str, journey: str, session: str,
                                            mean: float, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte,mean,credit FROM {table} WHERE mean >= {mean} and credit >= {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean_and_credit_inf(self, schema: str, semester: str, journey: str, session: str,
                                            mean: float, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte,mean,credit FROM {table} WHERE mean >= {mean} and credit <= {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_credit(self, schema: str, semester: str, journey: str, session: str, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte,credit FROM {table} WHERE credit = {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_credit_inf(self, schema: str, semester: str, journey: str, session: str, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte,credit FROM {table} WHERE credit < {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean(self, schema: str, semester: str, journey: str, session: str, mean: float):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte,mean FROM {table} WHERE mean >= {mean}")
        out = result.fetchall()
        conn.close()
        return out

    def update_note(self, semester: str, journey: str, session: str, num_carte: str, ue_in: Any):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        up = update(table=table)
        up = up.values(ue_in)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)

    def read_by_num_carte(self, semester: str, journey: str, session: str, num_carte: str) -> Any:
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def update_auto(self, semester: str, journey: str, session: str, num_carte: str):
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        table_norm = Table(f"note_{journey.lower()}_{semester.lower()}_normal", metadata, autoload=True)
        sel = table_norm.select()
        sel = sel.where(table_norm.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        up = table.update()
        up = up.values(out)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)
        conn.close()

    def read_by_credit(self, semester: str, journey: str, session: str, credit: int, year:str) -> Any:
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        sel = table.select()
        sel = sel.where(table.columns.credit < credit)
        sel = sel.where(table.columns.year == year)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_by_num_carte(self,semester: str, journey: str, session: str, num_carte: str):
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_carte == num_carte)
        conn.execute(dele)
        conn.close()

    def read_ue_mean(self, schema: str, semester: str, journey: str, session: str, num_carte: str,
                        obj_in: str) -> Any:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        sel = table.select()
        sel = sel.where(f"table.columns.{num_carte} == {num_carte}")
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


note = CRUDNote(MatierEC)
