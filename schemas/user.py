
from pydantic import BaseModel, EmailStr
from .appointment import Appointment

from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class User(UserBase):
    id: int
    is_superuser: bool = False
    appointments: list[Appointment] = []

    class Config:
        orm_mode = True
