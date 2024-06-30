from sqlalchemy.orm import Session
from fastapi import HTTPException

import schemas
from models import User
from .base import BaseCrud

from passlib.context import CryptContext
from typing import Type


class UserCrud(BaseCrud):
    def __init__(self, db: Session):
        super().__init__(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_users(self, skip, limit) -> list[Type[User]]:
        db_users = self._db.query(User).offset(skip).limit(limit).all()
        return db_users

    def get_user_by_email(self, email: str) -> User:
        db_user = self._db.query(User).filter(User.email == email).first()
        return db_user

    def get_user_by_id(self, user_id: int) -> User:
        db_user = self._db.query(User).filter(User.id == user_id).first()
        return db_user

    def create_user(self, user: schemas.UserCreate) -> User:
        try:
            db_user = self.get_user_by_email(user.email)
            if db_user:
                raise HTTPException(status_code=400, detail="User already exists")
            hashed_password = self.pwd_context.hash(user.password)

            db_user = User(
                email=user.email,
                name=user.name,
                password_hash=hashed_password,
                phone=user.phone
            )

            self._db.add(db_user)
            self._db.commit()
            self._db.refresh(db_user)
            return db_user

        except Exception as e:
            self._db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_user(self, user_id: int, user: schemas.UserUpdate) -> User:
        db_user = self.get_user_by_id(user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            for key, value in user.dict().items():
                if value:
                    setattr(db_user, key, value)

            self._db.commit()
            self._db.refresh(db_user)
            return db_user

        except Exception as e:
            self._db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        self._db.delete(db_user)
        self._db.commit()
        return {"detail": "User deleted"}
