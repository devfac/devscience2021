from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .role import Role  # noqa: F401
    from .mention import Mention  # noqa: F401


class User(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
    uuid_role = Column(UUID(as_uuid=True), ForeignKey("role.uuid"))
    uuid_mention = Column(UUID(as_uuid=True), ForeignKey("mention.uuid"))
    role = relationship("Role", back_populates="user")
    mention = relationship("Mention", back_populates="user")

