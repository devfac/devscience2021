import uuid

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy.sql.sqltypes import ARRAY

from app.db.base_class import Base


class Publication(Base):
    uuid = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    url_file = Column(ARRAY(String))
    type = Column(String)
    visibility = Column(ARRAY(String))
    created_at = Column(String, nullable=False)
    description = Column(String, nullable=False)
    expiration_date = Column(Date)
