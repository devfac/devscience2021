import uuid

from sqlalchemy import Column, String, FLOAT
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class CollegeYear(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    code = Column(String)
    mean = Column(FLOAT)
