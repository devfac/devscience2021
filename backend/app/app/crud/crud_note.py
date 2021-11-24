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

    def check_table_exist(self,schemas:str, semestre:str, parcours:str) -> bool:
        metadata = MetaData(bind=engine, schema=schemas)
        for table in metadata.sorted_tables:
            if table.name == f"note_{semestre}_{parcours}":
                return True
        return False


    def insert_note(self,db:Session, schema: str,semestre:str,parcours:str, num_carte:str) -> Optional[MatierEC]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{semestre}_{parcours}", metadata,autoload=True)
        ins = insert(table=table)
        ins = ins.values({f"num_carte:{num_carte}"})
        db.execute(ins)
        db.close
        sel = table.select()
        result = db.execute(sel)
        out = result.fetchall()
        db.close()
        return out


    def update_note(self,db:Session,schema: str, semestre:str, parcours:str, num_carte:str, obj_in:str) -> Optional[MatierEC]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{semestre}_{parcours}", metadata,autoload=True)
        up = update(table=table)
        up = up.values(obj_in_data)
        up = up.where(table.c.num_carte == num_carte)
        db.execute(up)
        db.close
        sel = table.select()
        result = db.execute(sel)
        out = result.fetchall()
        db.close()
        return out

    def read_by_num_carte(self,db:Session,schema: str, semestre:str, parcours:str, num_carte:str, obj_in:str) -> Any:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{semestre}_{parcours}", metadata,autoload=True)
        sel = table.select()
        sel = sel.where(table.c.num_carte == num_carte)
        result = db.execute(sel)
        out = result.fetchone()
        db.close()
        return out
        

note = CRUDNote(MatierEC)
