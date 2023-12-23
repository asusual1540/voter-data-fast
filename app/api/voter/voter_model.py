from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class Area(Base):
    __tablename__ = 'areas'

    id = Column(String, primary_key=True, index=True)
    gender = Column(String(1000), default=None, nullable=False)
    district = Column(String(1000), default=None, nullable=False)
    sub_district = Column(String(1000), default=None, nullable=False)
    city_corporation = Column(String(1000), default=None, nullable=False)
    union = Column(String(1000), default=None, nullable=False)
    ward_no = Column(Integer, default=None, nullable=False)
    voter_area = Column(String(1000), default=None, nullable=False)
    total_voter = Column(Integer, default=None, nullable=False)
    voter_area_no = Column(String(1000), default=None, nullable=False)
    total_voter_female = Column(Integer, default=None, nullable=False)

    voters = relationship("Voter", back_populates="area")

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Voter(Base):
    __tablename__ = 'voters'

    id = Column(String, primary_key=True, index=True)
    name = Column(String(1000), default=None, nullable=False)
    voter_no = Column(String(1000), default=None, nullable=False)
    father_name = Column(String(1000), default=None, nullable=False)
    mother_name = Column(String(1000), default=None, nullable=False)
    occupation = Column(String(1000), default=None, nullable=False)
    address = Column(String(1000), default=None, nullable=False)

    area_id = Column(String, ForeignKey('areas.id'))
    area = relationship("Area", back_populates="voters")

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class VoterCreate(BaseModel):
    name: str
    voter_no: str
    father_name: str
    mother_name: str
    occupation: str
    address: str
    area_id: str


class AreaCreate(BaseModel):
    gender: str
    district: str
    sub_district: str
    city_corporation: str
    union: str
    ward_no: int
    voter_area: str
    total_voter: int
    voter_area_no: str
    total_voter_female: int