import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# work with db and models
from sqlalchemy.orm import Session
from database import get_db
import models

# work with jwt token
from jose import JWTError, jwt

# work with time
from datetime import datetime, timedelta

# working with schemas
from schemas import TokenData

path = "../.env"
load_dotenv(path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/login/user", scheme_name="user_oauth2_schema")
oauth2_scheme_doctor = OAuth2PasswordBearer(tokenUrl="/login/doctor", scheme_name="doctor_oauth2_schema")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_scheme_user),
    db: Session = Depends(get_db),
    credentials_exception=HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
):
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()

    return user


def get_current_doctor(
    token: str = Depends(oauth2_scheme_doctor),
    db: Session = Depends(get_db),
    credentials_exception=HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
):
    token = verify_access_token(token, credentials_exception)
    doctor = db.query(models.Doctor).filter(models.Doctor.id == token.user_id).first()

    return doctor


def get_current_super_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_super_user:
        raise HTTPException(403, "Permission denied")
    return current_user
