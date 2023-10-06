from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .student import Student  # noqa: F401


class Validation(Base):
    id = Column(Integer, primary_key=True, index=True)
    semester = Column(String(20))
    session = Column(String(250))
    id_year = Column(Integer, ForeignKey("college_year.id"))
    mean = Column(Float)
    credit = Column(Integer)
    id_journey = Column(Integer, ForeignKey("journey.id"))
    num_carte = Column(String(50), ForeignKey("student.num_carte"))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    student = relationship("Student")
    journey = relationship("Journey")
    year = relationship("CollegeYear")
