from typing import List, Optional

from sqlalchemy import text
from uuid import UUID
from sqlalchemy.inspection import inspect

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from app.crud.base import CRUDBase
from app.schemas.etudiant import EtudiantAncienCreate, EtudiantAncienUpdate,EtudiantAncien
from app.db.session import engine


class CRUDEtudiantAncien(CRUDBase[EtudiantAncien, EtudiantAncienCreate, EtudiantAncienUpdate]):

    def update_etudiant(self,schema: str, num_carte: str, obj_in: EtudiantAncienUpdate) -> Optional[EtudiantAncien]:
        obj_in.num_carte = num_carte
        obj_in_data = jsonable_encoder(obj_in)
        update = text(f""" UPDATE "{schema}"."ancien_etudiant" SET 
                nom=:nom,prenom=:prenom,date_naiss=:date_naiss,lieu_naiss=:lieu_naiss,
                adresse=:adresse,sexe=:sexe,nation=:nation,
                num_cin=:num_cin,date_cin=:date_cin,lieu_cin=:lieu_cin,montant=:montant,
                num_quitance=:num_quitance,date_quitance=:date_quitance,etat=:etat,
                photo=:photo,moyenne=:moyenne,bacc=:bacc,uuid_mention=:uuid_mention,
                uuid_parcours=:uuid_parcours,semestre_petit=:semestre_petit,
                semestre_grand=:semestre_grand 
                WHERE num_carte = :num_carte 
            """)
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" """)
        with engine.begin() as con:
            con.execute(update,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row

    def get_by_num_carte(self, schema: str, num_carte: str) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE num_carte= :num_carte
        """)
        with engine.begin() as con:
           row = con.execute(select, {"num_carte":num_carte}).fetchone()
           return row

    def get_by_mention(self, schema: str, uuid_mention: UUID) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE uuid_mention= :uuid_mention
        """)
        with engine.begin() as con:
           row = con.execute(select, {"uuid_mention":uuid_mention}).fetchall()
           return row

    def get_by_parcours(self, schema: str, uuid_parcours: UUID) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE uuid_parcours= :uuid_parcours
        """)
        with engine.begin() as con:
           row = con.execute(select, {"uuid_parcours":uuid_parcours}).fetchall()
           return row

    def get_by_class(self, schema: str, uuid_parcours: UUID, uuid_mention: UUID, semestre: str) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE uuid_parcours= :uuid_parcours 
        AND uuid_mention =: uuid_mention AND (semetre_petit= :semetrse OR semestre_grand =: semestre)
        """)
        with engine.begin() as con:
           row = con.execute(select, 
           {"uuid_parcours":uuid_parcours,"uuid_mention":uuid_mention,"semestre":semestre}).fetchall()
           return row

    def get_by_semetre_and_mention(self, schema: str,uuid_mention:UUID, semestre_grand: str) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE uuid_mention= :uuid_mention 
        AND semestre_grand= :semestre_grand
        """)
        with engine.begin() as con:
           row = con.execute(select, {"semestre_grand":semestre_grand , "uuid_mention":uuid_mention}).fetchall()
           return row

    def get_by_etat(self, schema: str,etat: str) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE etat= :etat 
        """)
        with engine.begin() as con:
           row = con.execute(select, {"etat":etat }).fetchall()
           return row

    def get_by_etat_and_moyenne(self, schema: str,etat: str, moyenne: float) -> Optional[EtudiantAncien]:
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" WHERE etat= :etat AND moyenne >= :moyenne
        """)
        with engine.begin() as con:
           row = con.execute(select, {"etat":etat,"moyenne":moyenne }).fetchall()
           return row

    def create_etudiant(self,schema: str, obj_in: EtudiantAncienCreate) -> Optional[EtudiantAncien]:
        obj_in_data = jsonable_encoder(obj_in)
        insert = text(f"""
        INSERT INTO "{schema}"."ancien_etudiant" (
            "uuid", "num_carte", "nom", "prenom", "date_naiss", "lieu_naiss", "adresse", "sexe",
            "nation", "num_cin", "date_cin","lieu_cin", "montant", "num_quitance", "date_quitance",
            "etat", "photo", "moyenne", "bacc", "uuid_mention", "uuid_parcours", "semestre_petit",
            "semestre_grand")
            VALUES
            (:uuid,:num_carte,:nom,:prenom,:date_naiss,:lieu_naiss,:adresse,:sexe,:nation,
                :num_cin,:date_cin,:lieu_cin,:montant,:num_quitance,:date_quitance,:etat,
                :photo,:moyenne,:bacc,:uuid_mention,:uuid_parcours,:semestre_petit,
                :semestre_grand); """)
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" """)
        with engine.begin() as con:
            con.execute(insert,obj_in_data)
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
        return row

    def get_all(self,schema: str) -> Optional[EtudiantAncien]:
        insert = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant"
        """)
        with engine.begin() as con:
           row = con.execute(insert).fetchall()
           return row

    def delete_etudiant(self,schema: str, num_carte: str) -> Optional[EtudiantAncien]:
        delete = text(f"""
        DELETE FROM "{schema}"."ancien_etudiant" WHERE num_carte = :num_carte
        """)
        select = text(f"""
        SELECT * FROM "{schema}"."ancien_etudiant" """)
        with engine.begin() as con:
           con.execute(delete, {"num_carte":num_carte})
        with engine.begin() as con2:
           row = con2.execute(select).fetchall()
           return row
        


ancien_etudiant = CRUDEtudiantAncien(EtudiantAncien)
