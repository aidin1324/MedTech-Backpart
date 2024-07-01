from fastapi import HTTPException

from .base import BaseCrud
from .dtimeslot import DtimeSlotCrud
from sqlalchemy.orm import Session
from models import Appointment


class AppointmentCrud(BaseCrud):
    def __init__(self, db: Session):
        super().__init__(db)
        self.DtimeSlotCrud = DtimeSlotCrud(db=db)

    def get_all_appointments(self, skip: int = 0, limit: int = 100):
        db_appointments = self._db.query(Appointment).offset(skip).limit(limit).all()
        return db_appointments

    def get_appointment_by_id(self, app_id: int) -> Appointment:
        db_appointment = self._db.query(Appointment).filter(Appointment.id == app_id).first()
        return db_appointment

    def get_patient_appointments(self, patient_id: int):
        db_appointments = self._db.query(Appointment).filter(
            Appointment.patient_id == patient_id
        ).all()
        return db_appointments

    def get_appointment_by_spec_id(self, patient_id: int, time_slot_id: int):
        db_appointment = self._db.query(Appointment).filter(
    Appointment.patient_id == patient_id,
            Appointment.time_slot_id == time_slot_id
        ).first()
        return db_appointment

    def create_appointment(self, patient_id: int, time_slot_id: int):
        db_appointment = self.get_appointment_by_spec_id(patient_id, time_slot_id)
        if db_appointment:
            raise HTTPException(status_code=400, detail="already exist")
        db_time_slot = self.DtimeSlotCrud.get_timeslot_by_id(time_slot_id)
        if not db_time_slot.is_available:
            raise HTTPException(400, detail="timeslot is not available")
        db_appoint = Appointment(patient_id=patient_id, time_slot_id=time_slot_id)
        self._db.add(db_appoint)
        try:
            self._db.commit()
            self._db.refresh(db_appoint)
        except Exception as e:
            self._db.rollback()
            raise e

        # Update time slot availability
        db_time_slot.is_available = False
        try:
            self._db.commit()
            self._db.refresh(db_time_slot)
        except Exception as e:
            self._db.rollback()
            raise e

        return db_appoint

    def delete_appointment(self, app_id: int, patient_id: int):
        db_appoint = self.get_appointment_by_id(app_id)
        if not db_appoint:
            raise HTTPException(400, detail="does not exist")

        if db_appoint.patient_id != patient_id:
            raise HTTPException(400, detail="Not authorized")

        self._db.delete(db_appoint)
        self._db.commit()

        db_time_slot = self.DtimeSlotCrud.get_timeslot_by_id(db_appoint.time_slot_id)
        db_time_slot.is_available = True
        try:
            self._db.commit()
            self._db.refresh(db_time_slot)
        except Exception as e:
            self._db.rollback()
            raise e
        return {"detail": "deleted successfully"}