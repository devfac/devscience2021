from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.db.base_class import Base

if TYPE_CHECKING:
    from .student import Student  # noqa: F401


class Validation(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    semester = Column(String)
    session = Column(String)
    year = Column(String)
    mean = Column(Float)
    credit = Column(Integer)
    uuid_journey = Column(UUID(as_uuid=True), ForeignKey("journey.uuid"))
    num_carte = Column(String, ForeignKey("student.num_carte"))

    student = relationship("Student")
    journey = relationship("Journey")
