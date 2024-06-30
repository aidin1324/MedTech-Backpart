from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    phone = Column(String)
    license_number = Column(String, default="TEST123")
    license_expiry_date = Column(Date, default="06.06.2040")

    time_slots = relationship("DoctorTimeSlot", back_populates="doctor")
