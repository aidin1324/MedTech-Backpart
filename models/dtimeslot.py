from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class DtimeSlot(Base):
    __tablename__ = "doctor_time_slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    start_time = Column(String)
    end_time = Column(String)
    is_available = Column(Boolean, default=True)
    is_lunch_break = Column(Boolean, default=False)
    date = Column(DateTime, index=True)

    doctor = relationship("Doctor", back_populates="time_slots")
    appointments = relationship("Appointment", back_populates="day_schedule")
