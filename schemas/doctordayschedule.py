from pydantic import BaseModel

from typing import Optional
from .appointment import Appointment
from datetime import datetime


class DoctorDayScheduleBase(BaseModel):
    start_time: datetime
    end_time: datetime
    is_available: Optional[bool] = True
    is_lunch_break: Optional[bool] = True


class DoctorDayScheduleCreate(DoctorDayScheduleBase):
    pass


class DoctorDayScheduleUpdate(DoctorDayScheduleBase):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_available: Optional[bool] = None
    is_lunch_break: Optional[bool] = None


class DoctorDaySchedule(DoctorDayScheduleBase):
    id: int
    doctor_id: int
    appointments: list[Appointment] = []

    class Config:
        orm_mode = True
