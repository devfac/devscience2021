from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .semestre import Semestre  # noqa: F401
    from .anne_univ import AnneUniv



class SemestreValide(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num_carte = Column(String)
    semestre = Column(ARRAY(String))
    anne = Column(ARRAY(String))

