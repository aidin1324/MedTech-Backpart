from pydantic import BaseModel, EmailStr


class LogtoSystem(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "email": "aidinror@gmail.com",
            "password": "adi123123"
        }