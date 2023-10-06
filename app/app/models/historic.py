from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text, DATETIME, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Historic(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(250), ForeignKey("user.email"))
    title = Column(String(250))
    value = Column(Text)
    action = Column(Text)
    id_year = Column(Integer, ForeignKey("college_year.id"))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    user = relationship("User", foreign_keys=[email])
    year = relationship("CollegeYear", foreign_keys=[id_year])
