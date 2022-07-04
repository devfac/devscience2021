import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY

from app.db.base_class import Base

if TYPE_CHECKING:
    from .journey import Journey  # noqa: F401
    from .mention import Mention  # noqa: F401
    from .college_year import AnneUniv  # noqa: F401


class Students(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num_carte = Column(String, unique=True),
    num_select = Column(String, nullable=False, primary_key=True),
    last_name = Column(String),
    first_name = Column(String),
    date_birth = Column(String),
    place_birth = Column(String),
    address = Column(String),
    sex = Column(String),
    situation = Column(String),
    telephone = Column(String),
    nation = Column(String),
    num_cin = Column(String),
    date_cin = Column(String),
    lieu_cin = Column(String),
    price_right = Column(String),
    type = Column(String),
    num_receipt = Column(String, unique=True),
    date_receipt = Column(String),
    photo = Column(String, unique=True),
    baccalaureate_num = Column(String),
    baccalaureate_centre = Column(String),
    baccalaureate_years = Column(String),
    baccalaureate_seri = Column(String),
    work = Column(String),

    father_name = Column(String),
    father_work = Column(String),
    mother_name = Column(String),
    mother_work = Column(String),
    parent_address = Column(String),

    level = Column(String),  # niveau
    plugged = Column(String),  # branche
    inf_semester = Column(String),
    sup_semester = Column(String),

    uuid_mention = Column(UUID(as_uuid=True), ForeignKey("mention.uuid")),
    uuid_journey = Column(UUID(as_uuid=True), ForeignKey("journey.uuid")),

    select = Column(Boolean, default=False),
    actual_years = Column(UUID(as_uuid=True), ForeignKey("college_year.uuid")),

    uuid_college_year = Column(ARRAY(String), ForeignKey("college_year.uuid"))

    mention = relationship("Mention", back_populates="student")
    journey = relationship("Journey", back_populates="student")
    anne_univ = relationship("AnneUniv", back_populates="student")
