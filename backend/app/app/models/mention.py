from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .journey import Journey  # noqa: F401


class Mention(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True)
    value = Column(String, unique=True)
    abbreviation = Column(String, unique=True)
    plugged = Column(String)
    last_num_carte = Column(Integer)
    journey = relationship("Journey", back_populates="mention")
