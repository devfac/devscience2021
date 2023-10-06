from sqlalchemy import Column, String, FLOAT, DATETIME, Integer, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.utils import _get_date


class CollegeYear(Base):
    __tablename__ = "college_year"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(10))
    code = Column(String(10))
    mean = Column(FLOAT)
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    subscription = relationship("Subscription", back_populates="year")
