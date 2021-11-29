from typing import Any, Dict, List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table
from app.crud.base import CRUDBase
from app.schemas.etudiant import EtudiantAncienCreate, EtudiantAncienUpdate,EtudiantAncien
from app.db.session import engine


class CRUDEtudiantAncien(CRUDBase[EtudiantAncien, EtudiantAncienCreate, EtudiantAncienUpdate]):

    def update_etudiant(self,schema: str, num_carte: str, obj_in: Optional[EtudiantAncienUpdate]) -> Optional[EtudiantAncien]:
        obj_in_data = jsonable_encoder(obj_in)
        update_data  = {}
        for field in obj_in_data:
            if obj_in_data[field]:
                update_data[field]= obj_in_data[field]
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        up = table.update()
        up = up.values(update_data)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_by_num_carte(self, schema: str, num_carte: str) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_mention(self, schema: str, uuid_mention: UUID) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_mention == uuid_mention)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_parcours(self, schema: str, uuid_parcours: UUID) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_parcours == uuid_parcours)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_class(self, schema: str, uuid_parcours: UUID,  semestre: str) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_parcours == uuid_parcours
                        and table.columns.semestre == semestre  )
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_semetre_and_mention(self, schema: str,uuid_mention:UUID, semestre_grand: str) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_mention == uuid_mention and table.columns.semestre_grand == semestre_grand )
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_etat(self, schema: str,etat: str) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.etat == etat)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_etat_and_moyenne(self, schema: str,etat: str, moyenne: float) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("ancien_etudiant", metadata,autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.moyenne == moyenne and table.columns.etat == etat)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def create_etudiant(self,schema: str, obj_in: EtudiantAncienCreate) -> Optional[EtudiantAncien]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("ancien_etudiant", metadata,autoload=True)
        ins = table.insert().values(obj_in_data)
        conn.execute(ins)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out

    def get_all(self,schema: str) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("ancien_etudiant", metadata,autoload=True)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_etudiant(self,schema: str, num_carte: str) -> Optional[EtudiantAncien]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("ancien_etudiant", metadata,autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_carte == num_carte)
        conn.execute(dele)
        sel = table.select()
        result = conn.execute(sel)
        out = result.fetchall()
        return out
        


ancien_etudiant = CRUDEtudiantAncien(EtudiantAncien)
