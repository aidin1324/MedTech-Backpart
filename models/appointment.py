from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    time_slot_id = Column(Integer, ForeignKey("doctor_time_slots.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    patient = relationship("User", back_populates="appointments")
    day_schedule = relationship("DoctorTimeSlot", back_populates="appointments")
