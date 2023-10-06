from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from app.utils import _get_date


class StudentReceipt(Base):
    __tablename__ = "student_receipt"
    id = Column(Integer, primary_key=True, index=True)
    num_carte = Column(String(50), ForeignKey("student.num_carte"))
    price = Column(Float)
    date = Column(Date)
    id_year = Column(Integer, ForeignKey("college_year.id"))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    student = relationship("Student", foreign_keys=[num_carte])

