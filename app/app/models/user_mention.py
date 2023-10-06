from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from ..utils import _get_date

if TYPE_CHECKING:
    from .role import Role  # noqa: F401
    from .mention import Mention  # noqa: F401


class UserMention(Base):
    __tablename__ = "user_mention"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    id_mention = Column(Integer, ForeignKey("mention.id"))

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    mention = relationship("Mention", foreign_keys=[id_mention])
    user = relationship("User", foreign_keys=[id_user])
