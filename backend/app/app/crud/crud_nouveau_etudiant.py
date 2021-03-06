from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.expression import false

from fastapi.encoders import jsonable_encoder
from sqlalchemy import MetaData, Table, and_
from app.crud.base import CRUDBase
from app.schemas.etudiant import EtudiantNouveauCreate, EtudiantNouveauUpdate, EtudiantNouveau, SelectEtudiantBase
from app.db.session import engine


class CRUDEtudiantNouveau(CRUDBase[EtudiantNouveau, EtudiantNouveauCreate, EtudiantNouveauUpdate]):

    def update_etudiant(self, schema: str, num_carte: str, obj_in: EtudiantNouveauUpdate) -> Optional[EtudiantNouveau]:
        obj_in_data = jsonable_encoder(obj_in)
        update_data = {}
        for field in obj_in_data:
            if obj_in_data[field]:
                update_data[field] = obj_in_data[field]
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        up = table.update()
        up = up.values(update_data)
        up = up.where(table.c.num_carte == num_carte)
        conn.execute(up)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def update_etudiant_select(self, schema: str, num_select: str, obj_in: SelectEtudiantBase) -> Optional[
        EtudiantNouveau]:
        obj_in_data = jsonable_encoder(obj_in)
        update_data = {}
        for field in obj_in_data:
            if obj_in_data[field] != "" and obj_in_data[field] is not None:
                update_data[field] = obj_in_data[field]
        print(obj_in_data)
        print(update_data)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        up = table.update()
        up = up.values(update_data)
        up = up.where(table.c.num_select == num_select)
        conn.execute(up)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_num_carte(self, schema: str, num_carte: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_num_select(self, schema: str, num_select: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.num_select == num_select)
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def get_by_num_select_admis(self, schema: str, branche: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(
            and_(table.columns.num_carte != "null", table.columns.select == "true", table.columns.branche == branche))
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_select_and_mention(self, schema: str, uuid_mention: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(and_(table.columns.select == "true", table.columns.uuid_mention == uuid_mention))
        sel = sel.order_by(table.columns.num_select.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_mention(self, schema: str, uuid_mention: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_mention == uuid_mention)
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_by_parcours(self, schema: str, uuid_parcours: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        table = Table("nouveau_etudiant", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(table.columns.uuid_parcours == uuid_parcours)
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def create_etudiant(self, schema: str, obj_in: EtudiantNouveauCreate) -> Optional[EtudiantNouveau]:
        obj_in_data = jsonable_encoder(obj_in)
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("nouveau_etudiant", metadata, autoload=True)
        ins = table.insert().values(obj_in_data)
        conn.execute(ins)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def get_all(self, schema: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("nouveau_etudiant", metadata, autoload=True)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_etudiant(self, schema: str, num_select: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("nouveau_etudiant", metadata, autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_select == num_select)
        conn.execute(dele)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_etudiant_not_select(self, schema: str) -> Optional[EtudiantNouveau]:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table("nouveau_etudiant", metadata, autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.select == False)
        conn.execute(dele)
        sel = table.select()
        sel = sel.order_by(table.columns.nom.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out


nouveau_etudiant = CRUDEtudiantNouveau(EtudiantNouveau)
