import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CollegeYear(Base):
    __tablename__ = "college_year"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    code = Column(String)
    mean = Column(FLOAT)
