from typing import List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from app.crud.base import CRUDBase
from app.schemas.matier import MatierUEUpdate, MatierUECreate,MatierUE
from app.db.session import engine


class CRUDMatierUE(CRUDBase[MatierUE, MatierUECreate, MatierUEUpdate]):

    def update_ue(self,schema: str, uuid: str, obj_in: MatierUEUpdate) -> Optional[MatierUE]:
        obj_in.uuid = uuid
        obj_in_data = jsonable_encoder(obj_in)
        update = text(f""" UPDATE "{schema}"."unite_enseing" SET 
                title=:title,value=:value,credit=:credit,semestre=:semestre,
                uuid_parcours=:uuid_parcours,uuid_mention=:uuid_mention
                WHERE uuid = :uuid 
            """)
        select = text(f"""
        SELECT * FROM "{schema}"."unite_enseing" """)
        with engine.begin() as con:
            con.execute(update,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row


    def get_by_class(self, schema: str, uuid_parcours: UUID, semestre: str) -> Optional[MatierUE]:
        select = text(f"""
        SELECT * FROM "{schema}"."unite_enseing" WHERE uuid_parcours= :uuid_parcours 
        AND semestre =: semestre
        """)
        with engine.begin() as con:
           row = con.execute(select, 
           {"uuid_parcours":uuid_parcours,"semestre":semestre}).fetchall()
           return row


    def get_by_title(self, schema: str, title: str, semestre:str, uuid_parcours:UUID) -> Optional[MatierUE]:
        select = text(f"""
        SELECT * FROM "{schema}"."unite_enseing" WHERE title= :title 
        AND semestre= :semestre AND uuid_parcours= :uuid_parcours
        """)
        with engine.begin() as con:
           row = con.execute(select, 
           {"uuid_parcours":uuid_parcours,"semestre":semestre, "title":title}).fetchone()
           return row


    def get_by_uuid(self, schema: str, uuid: UUID) -> Optional[MatierUE]:
        select = text(f"""
        SELECT * FROM "{schema}"."unite_enseing" WHERE uuid= :uuid
        """)
        with engine.begin() as con:
           row = con.execute(select, {"uuid":uuid}).fetchone()
           return row


    def create_ue(self,schema: str, obj_in: MatierUECreate) -> Optional[MatierUE]:
        obj_in_data = jsonable_encoder(obj_in)
        insert = text(f"""
        INSERT INTO "{schema}"."unite_enseing" (
            "uuid", "title", "value", "credit", "semestre", "uuid_parcours", "uuid_mention")
            VALUES
            (:uuid,:title,:value,:credit,:semestre,:uuid_parcours,:uuid_mention);
         """)
        select = text(f"""
        SELECT * FROM "{schema}"."unite_enseing" """)
        with engine.begin() as con:
            con.execute(insert,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row

    def get_all(self,schema: str) -> Optional[MatierUE]:
        insert = text(f"""
        SELECT * FROM "{schema}"."unite_enseing"
        """)
        with engine.begin() as con:
           row = con.execute(insert).fetchall()
           return row

    def delete_ue(self,schema: str, uuid: str) -> Optional[MatierUE]:
        delete = text(f"""
        DELETE FROM "{schema}"."unite_enseing" WHERE uuid = :uuid
        """)
        select = text(f"""
        SELECT * FROM "{schema}"."unite_enseing" """)
        with engine.begin() as con:
           con.execute(delete, {"uuid":uuid})
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
           return row
        


matier_ue = CRUDMatierUE(MatierUE)
