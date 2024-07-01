from pydantic import BaseModel

from datetime import datetime


class DayScheduleCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    date: datetime = datetime.today()
    appointment_duration: int = 20
    lunch_start: datetime
    lunch_end: datetime
    recess: int
