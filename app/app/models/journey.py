from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DATETIME, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .mention import Mention  # noqa: F401


class Journey(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    abbreviation = Column(String(20))
    id_mention = Column(Integer, ForeignKey("mention.id"))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    mention = relationship("Mention", back_populates="journey")
