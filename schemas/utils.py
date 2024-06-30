from pydantic import BaseModel


class DayScheduleCreate(BaseModel):
    appointment_time: float
    lunch_start: datetime
    lunch_end: datetime
    recess: float
