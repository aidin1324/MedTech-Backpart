from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
from schemas import DayScheduleCreate, DtimeSlot, DtimeSlotUpdate, DtimeSlotCreate
from database import get_db
from oauth2 import oauth2
import models

from crud import DtimeSlotCrud
from datetime import datetime

router = APIRouter(tags=["Doctor time slots"])


def get_dtimeslot_service(db: Session = Depends(get_db)):
    return DtimeSlotCrud(db=db)


@router.get("/", response_model=list[DtimeSlot])
def read_time_slots(
    skip: int = 0,
    limit: int = 100,
    d_timeslot_service: DtimeSlot = Depends(get_dtimeslot_service)
):
    db_slots = d_timeslot_service.get_time_slots(skip=skip, limit=limit)
    return db_slots


@router.get("/id/{id}", response_model=DtimeSlot)
def read_time_slots_by_id(
    id: int,
    d_timeslot_service: DtimeSlot = Depends(get_dtimeslot_service)
):
    db_slot = d_timeslot_service.get_timeslot_by_id(id)
    return db_slot


@router.get("/doctor/{doctor_id}", response_model=list[DtimeSlot])
def read_time_slots_by_doctor_id(
    doctor_id: int,
    d_timeslot_service: DtimeSlot = Depends(get_dtimeslot_service)
):
    db_slots = d_timeslot_service.get_timeslot_by_doctor_id(doctor_id)
    return db_slots


@router.get("/date/{date}", response_model=list[DtimeSlot])
def read_time_slots_by_date(
    date: str,
    d_timeslot_service: DtimeSlot = Depends(get_dtimeslot_service)
):
    db_slots = d_timeslot_service.get_timeslot_by_date(date)
    return db_slots


@router.post("/")
def create_time_slots(
    settings: schemas.DayScheduleCreate,
    d_timeslot_service: DtimeSlot = Depends(get_dtimeslot_service),
    current_doctor: models.Doctor = Depends(oauth2.get_current_doctor)
):
    db_slots = d_timeslot_service.create_time_slots(
        settings,
        doctor_id=current_doctor.id
    )
    return db_slots


@router.delete("/delete_by_date/{date}")
def delete_time_slots_by_date(
    date: str,
    d_timeslot_service: DtimeSlot = Depends(get_dtimeslot_service),
    current_doctor: models.Doctor = Depends(oauth2.get_current_doctor)
):
    db_slots_del = d_timeslot_service.delete_time_slots_by_date(date)
    return db_slots_del