import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, DateTime, Float, DATETIME, Integer, Date
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Permission(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), ForeignKey("user.email"))
    type = Column(String(256))
    email_sender = Column(String(256), ForeignKey("user.email"))
    expiration_date = Column(Date)
    accepted = Column(Boolean())

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    sender = relationship("User", foreign_keys=[email_sender])
    email_ = relationship("User", foreign_keys=[email])
