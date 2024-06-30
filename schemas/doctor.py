from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from .doctordayschedule import DoctorDaySchedule

class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: EmailStr
    phone: str


class DoctorCreate(DoctorBase):
    password: str


class DoctorUpdate(DoctorBase):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Doctor(DoctorBase):
    id: int
    license_number: str = "TEST123"
    license_expiry_date: datetime = datetime(2055, 6, 6)
    time_slots: list[DoctorDaySchedule] = []

    class Config:
        orm_mode = True
