import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql.base import UUID

from app.db.base_class import Base


class Semester(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
