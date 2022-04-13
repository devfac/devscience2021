from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
from app.core.config  import settings
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import engine

base = declarative_base()

class Test(base):
    __tablename__ = "test"
    __table_args__ = {"schema":settings.SCHEMAS}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)

def create_table():
    print(settings.SCHEMAS)
    Test.__table__.create(engine)
