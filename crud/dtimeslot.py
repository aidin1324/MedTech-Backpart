from sqlalchemy.orm import Session
from fastapi import HTTPException

import schemas
from models import DtimeSlot as Timeslot
from .base import BaseCrud

from typing import Type


class DoctorDayScheduleCrud(BaseCrud):
    """
    DoctorDaySchedule == timeslot
    """
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        
    def get_timeslot_by_id(self, timeslot_id: int) -> Timeslot:
        db_timeslot = self._db.query(Timeslot).filter(Timeslot.id == timeslot_id).first()
        return db_timeslot

