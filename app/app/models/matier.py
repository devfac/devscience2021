from sqlalchemy import Boolean, Column, Integer, String, Float, DATETIME, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from app.utils import _get_date


class TeachingUnit(Base):
    __tablename__ = "teaching_unit"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    value = Column(String(256))
    credit = Column(Integer)
    semester = Column(String(10))
    key_unique = Column(String(256))
    id_journey = Column(Integer, ForeignKey("journey.id"))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    journey = relationship("Journey", foreign_keys=[id_journey])


class ConstituentElement(Base):
    __tablename__ = "constituent_element"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    value = Column(String(256))
    weight = Column(Float)
    value_ue = Column(String(256))
    semester = Column(String(10))
    key_unique = Column(String(256))
    teacher = Column(String(256))
    is_optional = Column(Boolean)
    id_journey = Column(Integer, ForeignKey("journey.id"))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    journey = relationship("Journey",  foreign_keys=[id_journey])
