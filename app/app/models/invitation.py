from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, Text, Date, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Invitation(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), ForeignKey("user.email"))
    email_from = Column(String(256), ForeignKey("user.email"))
    message = Column(Text)
    is_ready = Column(Boolean(), default=False)

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    user = relationship("User", foreign_keys=[email])
