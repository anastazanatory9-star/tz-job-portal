from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)  # applicant / employer / admin
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=True)
    nida = Column(String, unique=True, nullable=True)
    firstName = Column(String)
    middleName = Column(String)
    lastName = Column(String)
    dob = Column(String)
    gender = Column(String)
    region = Column(String)
    district = Column(String)
    ward = Column(String)
    street = Column(String)
    house = Column(String)
    jobCategory = Column(String)
    eduLevel = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    chairman = Column(String)
    baloozi = Column(String)
    verified = Column(Boolean, default=False)
    otp = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
