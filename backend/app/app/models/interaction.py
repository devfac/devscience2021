import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY

from app.db.base_class import Base


class Validation(Base):
    __tablename__ = "validation"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    s1 = Column(String)
    s2 = Column(String)
    s3 = Column(String)
    s4 = Column(String)
    s5 = Column(String)
    s6 = Column(String)
    s7 = Column(String)
    s8 = Column(String)
    s9 = Column(String)
    s10 = Column(String)
    num_carte = Column(String, ForeignKey("student.num_carte"))
    student = relationship("Student", foreign_keys=[num_carte])


class Interaction(Base):
    __tablename__ = "interaction"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    s1 = Column(ARRAY(String))
    s2 = Column(ARRAY(String))
    s3 = Column(ARRAY(String))
    s4 = Column(ARRAY(String))
    s5 = Column(ARRAY(String))
    s6 = Column(ARRAY(String))
    s7 = Column(ARRAY(String))
    s8 = Column(ARRAY(String))
    s9 = Column(ARRAY(String))
    s10 = Column(ARRAY(String))
    college_year = Column(String)
    uuid_journey = Column(UUID(as_uuid=True), ForeignKey("journey.uuid"))

    journey = relationship("Journey", foreign_keys=[uuid_journey])


class Diploma(Base):
    __tablename__ = "diploma"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num_carte = Column(String, ForeignKey("student.num_carte"))
    licence_title = Column(String)
    master_title = Column(String)

    student = relationship("Student", foreign_keys='Diploma.num_carte')
