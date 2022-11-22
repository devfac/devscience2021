import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class Invitation(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, ForeignKey("user.email"))
    email_from = Column(String, ForeignKey("user.email"))
    message = Column(String)
    created_at = Column(DateTime)
    is_ready = Column(Boolean, default=False)
    user = relationship("User", foreign_keys=[email])