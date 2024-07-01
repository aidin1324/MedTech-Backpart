from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
from schemas import AppointmentCreate, Appointment
from database import get_db
from oauth2 import oauth2
import models

from crud import AppointmentCrud
from datetime import datetime

router = APIRouter(tags=["Appointments"])


def get_appointment_service(db: Session = Depends(get_db)):
    return AppointmentCrud(db=db)


@router.get("/", response_model=list[Appointment])
def read_appoints(
    skip: int = 0,
    limit: int = 100,
    appointment_service: Appointment = Depends(get_appointment_service)
):
    db_app = appointment_service.get_all_appointments(skip=skip, limit=limit)
    return db_app


@router.get("/id/{id}", response_model=Appointment)
def read_appointments_by_id(
    app_id: int,
    appointment_service: Appointment = Depends(get_appointment_service)
):
    db_app = appointment_service.get_appointment_by_id(app_id)
    return db_app


@router.get("/patient/appointments", response_model=list[Appointment])
def read_appointments_by_user_id(
    appointment_service: Appointment = Depends(get_appointment_service),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    db_apps = appointment_service.get_patient_appointments(current_user.id)
    return db_apps


@router.get("/patient/appointments/{time_slot_id}", response_model=list[Appointment])
def read_appointments_by_spec_id(
    time_slot_id: int,
    appointment_service: Appointment = Depends(get_appointment_service),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    db_apps = appointment_service.get_appointment_by_spec_id(current_user.id, time_slot_id)
    return db_apps


@router.post("/patient/appointments/{time_slot_id}", response_model=Appointment)
def create_appointments_by_id(
    time_slot_id: int,
    appointment_service: Appointment = Depends(get_appointment_service),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    db_app = appointment_service.create_appointment(current_user.id, time_slot_id)
    return db_app


@router.delete("/patient/appointments/{app_id}")
def delete_appointments_by_id(
    app_id: int,
    appointment_service: Appointment = Depends(get_appointment_service),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    db_app_del = appointment_service.delete_appointment(app_id, current_user.id)
    return db_app_del