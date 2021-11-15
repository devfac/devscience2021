from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.schemas.etudiant import EtudiantNouveauCreate, EtudiantNouveauUpdate,EtudiantNouveau
from app.db.session import engine


class CRUDEtudiantNouveau(CRUDBase[EtudiantNouveau, EtudiantNouveauCreate, EtudiantNouveauUpdate]):

    def update_etudiant(self,schema: str, num_insc: str, obj_in: EtudiantNouveauUpdate) -> Optional[EtudiantNouveau]:
        obj_in.num_insc = num_insc
        obj_in_data = jsonable_encoder(obj_in)
        update = text(f""" UPDATE "{schema}"."nouveau_etudiant" SET 
                nom=:nom,prenom=:prenom,date_naiss=:date_naiss,lieu_naiss=:lieu_naiss,
                adresse=:adresse,sexe=:sexe,nation=:nation,
                num_cin=:num_cin,date_cin=:date_cin,lieu_cin=:lieu_cin,montant=:montant,
                num_quitance=:num_quitance,date_quitance=:date_quitance,situation=:situation,
                photo=:photo,niveau=:niveau,bacc_num=:bacc_num,bacc_anne=:bacc_anne,
                bacc_centre=:bacc_centre,bacc_serie=:bacc_serie,nom_pere=:nom_pere,
                proffession_pere=:proffession_pere,nom_mere=:nom_mere,proffession_mere=:proffession_mere,
                adresse_parent=:adresse_parent,uuid_mention=:uuid_mention,uuid_parcours=:uuid_parcours
                WHERE num_insc = :num_insc
            """)
        select = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant" """)
        with engine.begin() as con:
            con.execute(update,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row
    

    def get_by_num_insc(self, schema: str, num_insc: str) -> Optional[EtudiantNouveau]:
        select = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant" WHERE num_insc= :num_insc
        """)
        with engine.begin() as con:
           row = con.execute(select, {"num_insc":num_insc}).fetchone()
           return row

    def get_by_mention(self, schema: str, uuid_mention: str) -> Optional[EtudiantNouveau]:
        select = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant" WHERE uuid_mention= :uuid_mention
        """)
        with engine.begin() as con:
           row = con.execute(select, {"uuid_mention":uuid_mention}).fetchall()
           return row

    def get_by_parcours(self, schema: str, uuid_parcours: str) -> Optional[EtudiantNouveau]:
        select = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant" WHERE uuid_parcours= :uuid_parcours
        """)
        with engine.begin() as con:
           row = con.execute(select, {"uuid_parcours":uuid_parcours}).fetchall()
           return row


    def create_etudiant(self,schema: str, obj_in: EtudiantNouveauCreate) -> Optional[EtudiantNouveau]:
        obj_in_data = jsonable_encoder(obj_in)
        insert = text(f"""
        INSERT INTO "{schema}"."nouveau_etudiant" (
            "uuid", "num_insc", "nom", "prenom", "date_naiss", "lieu_naiss", "adresse", "sexe",
            "nation", "num_cin", "date_cin","lieu_cin", "montant", "num_quitance", "date_quitance", "situation",
            "telephone", "proffession", "photo", "niveau", "bacc_num", "bacc_anne", "bacc_centre", "bacc_serie", 
            "nom_pere", "proffession_pere", "nom_mere", "proffession_mere", "adresse_parent",
            "uuid_mention", "uuid_parcours")
            VALUES
            (:uuid,:num_insc,:nom,:prenom,:date_naiss,:lieu_naiss,:adresse,:sexe,
            :nation, :num_cin,:date_cin,:lieu_cin,:montant,:num_quitance,:date_quitance,:situation,
            :telephone, :proffession,:photo,:niveau,:bacc_num,:bacc_anne, :bacc_serie, :bacc_centre,
            :nom_pere, :proffession_pere, :nom_mere, :proffession_mere, :adresse_parent, 
            :uuid_mention,:uuid_parcours); """)
        select = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant" """)
        with engine.begin() as con:
            con.execute(insert,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row

    def get_all(self,schema: str) -> Optional[EtudiantNouveau]:
        insert = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant"
        """)
        with engine.begin() as con:
           row = con.execute(insert).fetchall()
           return row

    def delete_etudiant(self,schema: str, num_insc: str) -> Optional[EtudiantNouveau]:
        delete = text(f"""
        DELETE FROM "{schema}"."nouveau_etudiant" WHERE num_insc = :num_insc
        """)
        select = text(f"""
        SELECT * FROM "{schema}"."nouveau_etudiant" """)
        with engine.begin() as con:
           con.execute(delete, {"num_insc":num_insc})
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
           return row
        


nouveau_etudiant = CRUDEtudiantNouveau(EtudiantNouveau)
