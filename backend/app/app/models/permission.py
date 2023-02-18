import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401

class Permission(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, ForeignKey("user.email"))
    type = Column(String)
    email_sender = Column(String, ForeignKey("user.email"))
    expiration_date = Column(DateTime(timezone=True))
    accepted = Column(Boolean)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    sender = relationship("User", foreign_keys=[email_sender])
    email_ = relationship("User", foreign_keys=[email])