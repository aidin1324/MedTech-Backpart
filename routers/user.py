from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import User, UserCreate, UserUpdate
from database import get_db

from crud import UserCrud

router = APIRouter(tags=["User"])


def get_user_service(db: Session = Depends(get_db)):
    return UserCrud(db=db)


@router.post("/registration", response_model=User)
def create_user(
    user: UserCreate,
    user_service: UserCrud = Depends(get_user_service),
):
    db_user = user_service.create_user(user)
    return db_user


@router.get("/", response_model=list[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserCrud = Depends(get_user_service)
):
    db_users = user_service.get_users(skip=skip, limit=limit)
    return db_users


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    user_service: UserCrud = Depends(get_user_service)
):
    db_user = user_service.get_user_by_id(user_id)
    return db_user


@router.patch("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    user_service: UserCrud = Depends(get_user_service)
):
    db_user = user_service.update_user(user_id, user)
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user_service: UserCrud = Depends(get_user_service)
):
    db_user = user_service.delete_user(user_id)
    return db_user
