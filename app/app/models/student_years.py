from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from app.utils import _get_date


class StudentYears(Base):
    __tablename__="student_years"
    id = Column(Integer, primary_key=True, index=True)
    id_year = Column(Integer, ForeignKey("college_year.id"))
    num_carte = Column(String(50), ForeignKey("student.num_carte"))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    student = relationship("Student", foreign_keys=[num_carte])
    year = relationship("CollegeYear", foreign_keys=[id_year])

