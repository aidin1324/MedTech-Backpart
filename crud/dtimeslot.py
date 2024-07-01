from sqlalchemy.orm import Session
from sqlalchemy import extract
from fastapi import HTTPException

import schemas
from models import DtimeSlot
from .base import BaseCrud

from typing import Type

from datetime import datetime, timedelta


class DtimeSlotCrud(BaseCrud):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def generate_schedule(
            self,
            start_time,
            end_time,
            date,
            appointment_duration,
            lunch_start,
            lunch_end,
            recess,
            doctor_id
    ):
        current_time = start_time
        schedule = []

        while current_time.strftime("%H-%M") < end_time.strftime("%H-%M"):
            if current_time >= lunch_start and current_time < lunch_end:
                time_slot = DtimeSlot(
                    doctor_id=doctor_id,
                    start_time=lunch_start.strftime("%H-%M"),
                    end_time=lunch_end.strftime("%H-%M"),
                    date=date,
                    is_available=False,
                    is_lunch_break=True
                )
                schedule.append(time_slot)
                current_time = lunch_end
                self._db.add(time_slot)
                self._db.commit()
                self._db.refresh(time_slot)
                continue

            end_appointment_time = current_time + timedelta(minutes=appointment_duration)

            if end_appointment_time > end_time:
                break

            if end_appointment_time > lunch_start and current_time < lunch_end:
                current_time = lunch_end
                continue

            time_slot = DtimeSlot(
                doctor_id=doctor_id,
                start_time=current_time.strftime("%H-%M"),
                end_time=end_appointment_time.strftime("%H-%M"),
                date=date
            )
            self._db.add(time_slot)
            self._db.commit()
            self._db.refresh(time_slot)
            schedule.append(time_slot)

            current_time = end_appointment_time + timedelta(minutes=recess)

        return schedule

    def get_time_slots(self, skip: int, limit: int) -> list[Type[DtimeSlot]]:
        db_time_slots = self._db.query(DtimeSlot).offset(skip).limit(limit).all()
        return db_time_slots

    def get_timeslot_by_id(self, timeslot_id: int) -> DtimeSlot:
        db_timeslot = self._db.query(DtimeSlot).filter(DtimeSlot.id == timeslot_id).first()
        return db_timeslot

    def get_timeslot_by_doctor_id(self, doctor_id: int) -> list[Type[DtimeSlot]]:
        db_timeslot = self._db.query(DtimeSlot).filter(DtimeSlot.doctor_id == doctor_id).all()
        return db_timeslot

    def get_timeslot_by_date(self, date_str: str) -> list[Type[DtimeSlot]]:
        try:
            date_obj = datetime.fromisoformat(date_str)
        except ValueError:
            raise ValueError("Invalid date format. Must be in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)")
        db_timeslots = (
            self._db.query(DtimeSlot)
            .filter(extract('year', DtimeSlot.date) == date_obj.year)
            .filter(extract('month', DtimeSlot.date) == date_obj.month)
            .filter(extract('day', DtimeSlot.date) == date_obj.day)
            .all()
        )
        return db_timeslots

    def create_time_slots(self, settings: schemas.DayScheduleCreate, doctor_id: int) -> list[DtimeSlot]:
        if settings.date.strftime("%Y-%m-%d") < datetime.now().strftime("%Y-%m-%d"):
            raise HTTPException(400, detail="you cannot plan day that gone")

        get_timeslot = self.get_timeslot_by_date(str(settings.date))
        if len(get_timeslot) != 0:
            raise HTTPException(status_code=400, detail="That day already planned, you can change, if you want")

        schedule = self.generate_schedule(**settings.dict(), doctor_id=doctor_id)
        return schedule

    def delete_time_slots_by_date(self, date_obj: str):
        db_time_slots = self.get_timeslot_by_date(date_obj)
        if len(db_time_slots) == 0:
            raise HTTPException(400, detail="not found")

        for timeslot in db_time_slots:
            self._db.delete(timeslot)

        self._db.commit()
        return {"detail": "success"}
