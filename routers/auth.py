from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import schemas
import models
from utils import utils
from oauth2 import oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/user', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/doctor', response_model=schemas.Token)
def doctor_login(doctor_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.email == doctor_credentials.username).first()

    if doctor is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify_password(doctor_credentials.password, doctor.password_hash):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": doctor.id})

    return {"access_token": access_token, "token_type": "bearer"}