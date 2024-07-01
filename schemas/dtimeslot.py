from pydantic import BaseModel

from typing import Optional
from .appointment import Appointment
from datetime import datetime


class DtimeSlotBase(BaseModel):
    start_time: str
    end_time: str
    is_available: bool = True
    is_lunch_break: bool = False
    date: Optional[datetime] = datetime.now().date()


class DtimeSlotCreate(DtimeSlotBase):
    pass


class DtimeSlotUpdate(DtimeSlotBase):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_available: Optional[bool] = None
    is_lunch_break: Optional[bool] = None


class DtimeSlot(DtimeSlotBase):
    id: int
    doctor_id: int
    appointments: list[Appointment] = []

    class Config:
        orm_mode = True
