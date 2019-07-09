from sqlalchemy import Column, Integer, Text, Boolean

from model.entity_base import Base


class Profile(Base):

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    gender = Column(Text)
    country = Column(Text)
    city = Column(Text)
    state = Column(Text)
    height_cm = Column(Integer)
    age = Column(Integer)
    eye_color = Column(Text)
    body_type = Column(Text)
    hair_color = Column(Text)
    ethnicity = Column(Text)
    denomination = Column(Text)
    photo_urls = Column(Text)
    photoLocations = Column(Text)
    looking_for = Column(Text)
    church_name = Column(Text)
    church_attendance = Column(Text)
    church_raised_in = Column(Text)
    drink = Column(Text)
    smoke = Column(Text)
    willing_to_relocate = Column(Text)
    marital_status = Column(Text)
    have_children = Column(Boolean)
    want_children = Column(Text)
    education_level = Column(Text)
    profession = Column(Text)