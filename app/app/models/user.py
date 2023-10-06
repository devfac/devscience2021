from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .role import Role  # noqa: F401
    from .mention import Mention  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), index=True)
    last_name = Column(String(256))
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
    id_role = Column(Integer, ForeignKey("role.id"))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    role = relationship("Role", back_populates="user")

