from sqlalchemy.orm import Session
from fastapi import HTTPException

import schemas
from models import Doctor
from .base import BaseCrud

from typing import Type
from passlib.context import CryptContext


class DoctorCrud(BaseCrud):
    def __init__(self, db: Session):
        super().__init__(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_doctors(self, skip, limit) -> list[Type[Doctor]]:
        db_doctors = self._db.query(Doctor).offset(skip).limit(limit).all()
        return db_doctors

    def get_doctor_by_email(self, email: str) -> Doctor:
        db_doctor = self._db.query(Doctor).filter(Doctor.email == email).first()
        return db_doctor

    def get_doctor_by_id(self, doctor_id: int) -> Doctor:
        db_doctor = self._db.query(Doctor).filter(Doctor.id == doctor_id).first()
        return db_doctor

    def create_doctor(self, doctor: schemas.DoctorCreate) -> Doctor:
        try:
            db_doctor = self.get_doctor_by_email(doctor.email)
            if db_doctor:
                raise HTTPException(status_code=400, detail="Doctor already exists")
            hashed_password = self.pwd_context.hash(doctor.password)

            db_doctor = Doctor(
                email=doctor.email,
                name=doctor.name,
                password_hash=hashed_password,
                phone=doctor.phone
            )

            self._db.add(db_doctor)
            self._db.commit()
            self._db.refresh(db_doctor)
            return db_doctor

        except Exception as e:
            self._db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_doctor(self, doctor_id: int, doctor: schemas.DoctorUpdate) -> Doctor:
        db_doctor = self.get_doctor_by_id(doctor_id)
        if db_doctor is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        try:
            for key, value in doctor.dict().items():
                if value:
                    setattr(db_doctor, key, value)

            self._db.commit()
            self._db.refresh(db_doctor)
            return db_doctor

        except Exception as e:
            self._db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_doctor(self, doctor_id: int):
        db_doctor = self.get_doctor_by_id(doctor_id)
        self._db.delete(db_doctor)
        self._db.commit()
        return {"detail": "Doctor deleted"}

