from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import Doctor, DoctorCreate, DoctorUpdate
from database import get_db

from crud import DoctorCrud
from oauth2 import oauth2

router = APIRouter(tags=["Doctors"])


def get_doctor_service(db: Session = Depends(get_db)):
    return DoctorCrud(db=db)


@router.get("/", response_model=list[Doctor])
def read_doctors(
    skip: int = 0,
    limit: int = 100,
    doctor_service: DoctorCrud = Depends(get_doctor_service)
):
    db_doctors = doctor_service.get_doctors(skip=skip, limit=limit)
    return db_doctors


@router.get("/{doctor_id}", response_model=Doctor)
def read_doctor(
    doctor_id: int,
    doctor_service: DoctorCrud = Depends(get_doctor_service)
):
    db_doctor = doctor_service.get_doctor_by_id(doctor_id)
    return db_doctor


@router.post("/registration", response_model=Doctor)
def create_doctor(
    doctor: DoctorCreate,
    doctor_service: DoctorCrud = Depends(get_doctor_service),
    token: str = Depends(oauth2.get_current_super_user)
):
    db_doctor = doctor_service.create_doctor(doctor)
    return db_doctor


@router.patch("/{doctor_id}", response_model=Doctor)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    doctor_service: DoctorCrud = Depends(get_doctor_service)
):
    db_doctor = doctor_service.update_doctor(doctor_id, doctor)
    return db_doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    doctor_service: DoctorCrud = Depends(get_doctor_service)
):
    db_doctor = doctor_service.delete_doctor(doctor_id)
    return db_doctor


