from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DATETIME, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .mention import Mention  # noqa: F401


class JourneySemester(Base):
    __tablename__ = "journey_semester"
    id = Column(Integer, primary_key=True, index=True)
    id_journey = Column(Integer, ForeignKey("journey.id"))
    semester = Column(String(25))
    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    journey = relationship("Journey", foreign_keys=[id_journey])
