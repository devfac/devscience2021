from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Column, Integer, String, Float, Text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY
import uuid
from app.db.base_class import Base


class Student(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num_carte = Column(String, unique=True, primary_key=True)
    num_select = Column(String, nullable=True, unique=True)
    last_name = Column(String)
    first_name = Column(String)
    date_birth = Column(String)
    place_birth = Column(String)
    address = Column(String)
    sex = Column(String)
    situation = Column(String)
    telephone = Column(String)
    nation = Column(String)
    num_cin = Column(String)
    date_cin = Column(String)
    place_cin = Column(String)
    type = Column(String) # passant , redoublant
    receipt_list = Column(ARRAY(String))
    receipt = Column(String)
    photo = Column(String)
    baccalaureate_num = Column(String)
    baccalaureate_center = Column(String)
    baccalaureate_years = Column(String)
    baccalaureate_series = Column(String)
    work = Column(String)

    father_name = Column(String)
    father_work = Column(String)
    mother_name = Column(String)
    mother_work = Column(String)
    parent_address = Column(String)

    level = Column(String)  # niveau
    inf_semester = Column(String)
    sup_semester = Column(String)

    actual_years = Column(ARRAY(String))
    enter_years = Column(String)

    uuid_journey = Column(UUID(as_uuid=True), ForeignKey("journey.uuid"))
    uuid_mention = Column(UUID(as_uuid=True), ForeignKey("mention.uuid"))

    is_selected = Column(Boolean, default=False)
    mean = Column(Float)

    journey = relationship("Journey", foreign_keys=[uuid_journey])
    mention = relationship("Mention", foreign_keys=[uuid_mention])
