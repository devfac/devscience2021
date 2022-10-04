import uuid

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy.sql.sqltypes import ARRAY
from sqlalchemy.sql.sqltypes import Float

from app.db.session import engine


def create(schemas):
    # table des anciens etudiants
    base = MetaData()

    # table des unité d'enseignements
    unite_enseing = Table("unite_enseing", base,
                          Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                          Column("title", String),
                          Column("value", String),
                          Column("credit", Integer),
                          Column("semester", String),
                          Column("key_unique", String),
                          Column("uuid_journey", UUID(as_uuid=True)),
                          Column("uuid_mention", UUID(as_uuid=True)),
                          schema=schemas
                          )

    # table des elements costitutif
    element_const = Table("element_const", base,
                          Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                          Column("title", String),
                          Column("value", String),
                          Column("weight", Float),
                          Column("value_ue", String),
                          Column("users", String),
                          Column("key_unique", String),
                          Column("semester", String),
                          Column("is_optional", Boolean),
                          Column("uuid_journey", UUID(as_uuid=True)),
                          Column("uuid_mention", UUID(as_uuid=True)),
                          schema=schemas
                          )

    # semester valide

    semester_valide = Table("semester_valide", base,
                            Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                            Column("num_carte", String),
                            Column("semester", ARRAY(String)),
                            schema=schemas
                            )

    diplome = Table("diplome", base,
                    Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                    Column("num_carte", String),
                    Column("diplome", ARRAY(String)),
                    Column("uuid_journey", UUID(as_uuid=True)),
                    Column("uuid_mention", UUID(as_uuid=True)),
                    schema=schemas
                    )

    unite_enseing.create(engine)
    element_const.create(engine)
    semester_valide.create(engine)
    diplome.create(engine)


def add_column(schemas, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {schemas}.{table_name} ADD COLUMN {column_name} {column_type}')


def array_column(schemas, table_name, matiers):
    for matier in range(matiers):
        column = Column(matier, Float)
        add_column(schemas=schemas, table_name=table_name, column=column)


"""
inspector = Inspector.from_engine(engine)
table_name in inpector.get_table_name()
"""
