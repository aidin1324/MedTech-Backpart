from datetime import datetime

from pydantic import BaseModel

from typing import Optional


class AppointmentBase(BaseModel):
    pass


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(BaseModel):
    id: int
    patient_id: int
    time_slot_id: int

    class Config:
        orm_mode = True
