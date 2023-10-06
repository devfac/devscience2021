from sqlalchemy import Column, Integer, String, DATETIME, Date

from app.db.base_class import Base
from app.utils import _get_date


class Classroom(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    capacity = Column(Integer)