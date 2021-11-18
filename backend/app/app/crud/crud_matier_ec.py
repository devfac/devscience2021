from typing import List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from app.crud.base import CRUDBase
from app.schemas.matier import MatierECUpdate, MatierECCreate,MatierEC
from app.db.session import engine


class CRUDMatierEC(CRUDBase[MatierEC, MatierECCreate, MatierECUpdate]):

    def update_ec(self,schema: str, uuid: str, obj_in: MatierECUpdate) -> Optional[MatierEC]:
        obj_in.uuid = uuid
        obj_in_data = jsonable_encoder(obj_in)
        update = text(f""" UPDATE "{schema}"."element_const" SET 
                title=:title,value=:value,poids=:poids,semestre=:semestre,value_ec=:value_ec,
                utilisateur=:utilisateur,uuid_parcours=:uuid_parcours,uuid_mention=:uuid_mention
                WHERE uuid = :uuid 
            """)
        select = text(f"""
        SELECT * FROM "{schema}"."element_const" """)
        with engine.begin() as con:
            con.execute(update,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row


    def get_by_class(self, schema: str, uuid_parcours: UUID, semestre: str) -> Optional[MatierEC]:
        select = text(f"""
        SELECT * FROM "{schema}"."element_const" WHERE uuid_parcours= :uuid_parcours 
        AND semestre =: semestre
        """)
        with engine.begin() as con:
           row = con.execute(select, 
           {"uuid_parcours":uuid_parcours,"semestre":semestre}).fetchall()
           return row

    def create_ec(self,schema: str, obj_in: MatierECCreate) -> Optional[MatierEC]:
        obj_in_data = jsonable_encoder(obj_in)
        insert = text(f"""
        INSERT INTO "{schema}"."element_const" (
            "uuid", "title", "value", "poids", "semestre","value_ue","utilisateur", "uuid_parcours", "uuid_mention")
            VALUES
            (:uuid,:title,:value,:poids,:value_ue,:utilisateur,:semestre,:uuid_parcours,:uuid_mention);
         """)
        select = text(f"""
        SELECT * FROM "{schema}"."element_const" """)
        with engine.begin() as con:
            con.execute(insert,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row

    def get_all(self,schema: str) -> Optional[MatierEC]:
        insert = text(f"""
        SELECT * FROM "{schema}"."element_const"
        """)
        with engine.begin() as con:
           row = con.execute(insert).fetchall()
           return row

    def delete_ec(self,schema: str, uuid: str) -> Optional[MatierEC]:
        delete = text(f"""
        DELETE FROM "{schema}"."element_const" WHERE uuid = :uuid
        """)
        select = text(f"""
        SELECT * FROM "{schema}"."element_const" """)
        with engine.begin() as con:
           con.execute(delete, {"uuid":uuid})
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
           return row
        


matier_ec = CRUDMatierEC(MatierEC)
