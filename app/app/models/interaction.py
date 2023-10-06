from sqlalchemy import Column, String, DATETIME, Integer, Date
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from app.utils import _get_date


class Interaction(Base):
    __tablename__ = "interaction"
    id = Column(Integer, primary_key=True, index=True)
    s1 = Column(JSON)
    s2 = Column(JSON)
    s3 = Column(JSON)
    s4 = Column(JSON)
    s5 = Column(JSON)
    s6 = Column(JSON)
    s7 = Column(JSON)
    s8 = Column(JSON)
    s9 = Column(JSON)
    s10 = Column(JSON)
    id_year = Column(Integer, ForeignKey("college_year.id"))
    id_journey = Column(Integer, ForeignKey("journey.id"))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    journey = relationship("Journey", foreign_keys=[id_journey])
    year = relationship("CollegeYear", foreign_keys=[id_year])


class Diploma(Base):
    __tablename__ = "diploma"
    id = Column(Integer, primary_key=True, index=True)
    num_carte = Column(String(50), ForeignKey("student.num_carte"))
    licence_title = Column(String(256))
    master_title = Column(String(256))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    student = relationship("Student", foreign_keys='Diploma.num_carte')
