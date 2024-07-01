from datetime import datetime

from pydantic import BaseModel

from typing import Optional


class AppointmentBase(BaseModel):
    patient_id: int
    time_slot_id: int


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
