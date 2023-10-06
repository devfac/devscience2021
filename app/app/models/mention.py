from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DATETIME, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .journey import Journey  # noqa: F401


class Mention(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), unique=True)
    value = Column(String(256), unique=True)
    abbreviation = Column(String(20), unique=True)
    plugged = Column(String(250))
    last_num_carte = Column(Integer)
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    journey = relationship("Journey", back_populates="mention")
