from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.sql.schema import ForeignKey, MetaData, Table
from app.db.session import engine


def create(schemas):
        base =  MetaData()
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
        element_const = Table("element_const",base,
            Column("uuid",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column("title",String),
            Column("value",String),
            Column("poids",Float),
            Column("value_ue",String),
            Column("utilisateur",String),
            Column("semestre",String),
            Column("key_unique",String),
            Column("uuid_parcours",UUID(as_uuid=True)),
            Column("uuid_mention",UUID(as_uuid=True)),
            schema=schemas
        )
        unite_enseing.create(engine)
        element_const.create(engine)