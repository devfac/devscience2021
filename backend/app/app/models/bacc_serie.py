from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base


class BaccSerie(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    value = Column(String, unique=True)
