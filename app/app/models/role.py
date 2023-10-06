from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)
    user = relationship("User", back_populates="role")
