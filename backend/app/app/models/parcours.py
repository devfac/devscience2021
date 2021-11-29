from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .mention import Mention  # noqa: F401


class Parcours(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    abreviation = Column(String)
    uuid_mention = Column(UUID(as_uuid=True), ForeignKey("mention.uuid"))
    mention = relationship("Mention", back_populates="parcours")

