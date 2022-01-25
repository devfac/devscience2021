from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.sql.schema import ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Float
from app.db.session import engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.sqltypes import ARRAY


def create(schemas):
        # table des anciens etudiants
        base =  MetaData()
        ancien_etudiant = Table("ancien_etudiant",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("num_carte",String, unique=True),
            Column("nom",String),
            Column("prenom",String),
            Column("date_naiss",String),
            Column("lieu_naiss",String),
            Column("adresse",String),
            Column("sexe",String),
            Column("nation",String),
            Column("num_cin",String),
            Column("date_cin",String),
            Column("lieu_cin",String),
            Column("montant",String),
            Column("num_quitance",String,unique=True),
            Column("date_quitance",String),
            Column("etat",String),
            Column("photo",String,unique=True),
            Column("moyenne",Float),
            Column("bacc_anne",String),
            Column("uuid_mention",UUID(as_uuid=True)),
            Column("uuid_parcours",UUID(as_uuid=True)),
            Column("semestre_petit",String),
            Column("semestre_grand",String),
            schema=schemas
        )
        # table des nouveaux etudiants
        nouveau_etudiant = Table("nouveau_etudiant",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("num_carte",String, unique=True),
            Column("num_select",String, nullable=False, primary_key=True),
            Column("nom",String),
            Column("prenom",String),
            Column("date_naiss",String),
            Column("lieu_naiss",String),
            Column("adresse",String),
            Column("sexe",String),
            Column("situation",String),
            Column("telephone",String),
            Column("nation",String),
            Column("num_cin",String),
            Column("date_cin",String),
            Column("lieu_cin",String),
            Column("montant",String),
            Column("etat",String),
            Column("num_quitance",String,unique=True),
            Column("date_quitance",String),
            Column("photo",String,unique=True),
            Column("bacc_num",String),
            Column("bacc_centre",String),
            Column("bacc_anne",String),
            Column("bacc_serie",String),
            Column("proffession",String),
            Column("nom_pere",String),
            Column("proffession_pere",String),
            Column("nom_mere",String),
            Column("proffession_mere",String),
            Column("adresse_parent",String),
            Column("niveau",String),
            Column("branche",String),
            Column("uuid_mention",UUID(as_uuid=True)),
            Column("uuid_parcours",UUID(as_uuid=True)),
            Column("select",Boolean, default=False),
            schema=schemas
        )

        # table des unité d'enseignements
        unite_enseing = Table("unite_enseing",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("title",String),
            Column("value",String),
            Column("credit",Integer),
            Column("semestre",String),
            Column("key_unique",String),
            Column("uuid_parcours",UUID(as_uuid=True)),
            Column("uuid_mention",UUID(as_uuid=True)),
            schema=schemas
        )

        # table des elements costitutif
        element_const = Table("element_const",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("title",String),
            Column("value",String),
            Column("poids",Float),
            Column("value_ue",String),
            Column("utilisateur",String),
            Column("key_unique",String),
            Column("semestre",String),
            Column("uuid_parcours",UUID(as_uuid=True)),
            Column("uuid_mention",UUID(as_uuid=True)),
            schema=schemas
        )

        #semestre valide

        semestre_valide = Table("semestre_valide",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("num_carte",String),
            Column("semestre",ARRAY(String)),
            schema=schemas
        )

        diplome = Table("diplome",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("num_carte",String),
            Column("diplome",ARRAY(String)),
            Column("uuid_parcours",UUID(as_uuid=True)),
            Column("uuid_mention",UUID(as_uuid=True)),
            schema=schemas
        )

        unite_enseing.create(engine)
        element_const.create(engine)
        semestre_valide.create(engine)
        diplome.create(engine)
        ancien_etudiant.create(engine)
        nouveau_etudiant.create(engine)
        
def add_column(schemas, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {schemas}.{table_name} ADD COLUMN {column_name} {column_type}' )

def array_column(schemas, table_name, matiers):
    for matier in range(matiers):
        column = Column(matier,Float)
        add_column(schemas=schemas,table_name=table_name,column=column)


"""
inspector = Inspector.from_engine(engine)
table_name in inpector.get_table_name()
"""