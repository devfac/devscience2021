from sqlalchemy import Column, Integer, String, Float, ForeignKey, DATETIME, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.utils import _get_date


class EnrollmentFee(Base):
    __tablename__ = "enrollment_fee"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(50))
    price = Column(Float)
    id_year = Column(Integer, ForeignKey("college_year.id"))
    id_mention = Column(Integer, ForeignKey("mention.id"))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    mention = relationship("Mention", foreign_keys=[id_mention])
    year = relationship("CollegeYear", foreign_keys=[id_year])


