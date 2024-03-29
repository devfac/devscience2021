import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Historic(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, ForeignKey("user.email"))
    title = Column(String)
    value = Column(String)
    action = Column(String)
    college_year = Column(String)
    created_at = Column(DateTime)
    user = relationship("User", foreign_keys=[email])