from fastapi import FastAPI

import models
from database.database import engine
from routers import auth, user, doctor, dtimeslot, appoint
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)

app = FastAPI()


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user")
app.include_router(doctor.router, prefix="/doctor")
app.include_router(auth.router, prefix="/login")
app.include_router(dtimeslot.router, prefix="/timeslot")
app.include_router(appoint.router, prefix="/appointment")