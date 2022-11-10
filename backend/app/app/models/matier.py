import uuid

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, MetaData, Table

from app.db.base_class import Base
from app.db.session import engine


class TeachingUnit(Base):
    __tablename__ = "teaching_unit"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    value = Column(String)
    credit = Column(Integer)
    semester = Column(String)
    key_unique = Column(String)
    uuid_journey = Column(UUID(as_uuid=True), ForeignKey("journey.uuid"))
    journey = relationship("Journey", foreign_keys=[uuid_journey])


class ConstituentElement(Base):
    __tablename__ = "constituent_element"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    value = Column(String)
    weight = Column(Float)
    value_ue = Column(String)
    semester = Column(String)
    key_unique = Column(String)
    teacher = Column(String)
    is_optional = Column(Boolean)
    uuid_journey = Column(UUID(as_uuid=True), ForeignKey("journey.uuid"))
    journey = relationship("Journey",  foreign_keys=[uuid_journey])
