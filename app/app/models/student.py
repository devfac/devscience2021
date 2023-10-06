from sqlalchemy import Boolean, Column, Integer, String, Float, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base
from app.utils import _get_date


class Student(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    num_carte = Column(String(50), unique=True, primary_key=True)
    email = Column(String(256), unique=True)
    num_select = Column(String(50), nullable=True, unique=True)
    last_name = Column(String(256))
    first_name = Column(String(256))
    date_birth = Column(Date)
    place_birth = Column(String(256))
    address = Column(Text)
    sex = Column(String(256))
    situation = Column(String(256))
    telephone = Column(String(256))
    nation = Column(String(256))
    num_cin = Column(String(256))
    date_cin = Column(String(256))
    place_cin = Column(String(256))
    type = Column(String(256))  # passant , redoublant
    photo = Column(String(256))
    baccalaureate_num = Column(String(256))
    baccalaureate_center = Column(String(256))
    baccalaureate_years = Column(String(256))
    baccalaureate_series = Column(String(256))
    work = Column(String(256))

    father_name = Column(String(256))
    father_work = Column(String(256))
    mother_name = Column(String(256))
    mother_work = Column(String(256))
    parent_address = Column(Text)

    level = Column(String(256))  # niveau
    inf_semester = Column(String(20))
    sup_semester = Column(String(20))

    enter_years = Column(String(50))

    id_journey = Column(Integer, ForeignKey("journey.id"))
    id_mention = Column(Integer, ForeignKey("mention.id"))

    is_selected = Column(Boolean, default=False)
    mean = Column(Float)

    created_at = Column(Date, default=_get_date)
    updated_at = Column(Date, onupdate=_get_date)

    journey = relationship("Journey", foreign_keys=[id_journey])
    mention = relationship("Mention", foreign_keys=[id_mention])
    subscription = relationship("Subscription")
