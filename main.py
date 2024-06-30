from fastapi import FastAPI

import models
from database.database import engine
from routers import auth, user, doctor
models.Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(user.router, prefix="/user")
app.include_router(doctor.router, prefix="/doctor")
app.include_router(auth.router, prefix="/login")