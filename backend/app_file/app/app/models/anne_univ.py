from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base_class import Base

if TYPE_CHECKING:
    from .semestre_valide import SemestreValide  # noqa: F401

class AnneUniv(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    code = Column(String)
    moyenne = Column(FLOAT)
