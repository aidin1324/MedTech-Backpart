from datetime import datetime

from pydantic import BaseModel

from typing import Optional


class AppointmentBase(BaseModel):
    start_time: datetime
    end_time: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class Appointment(BaseModel):
    id: int
    patient_id: int
    time_slot_id: int

    class Config:
        orm_mode = True