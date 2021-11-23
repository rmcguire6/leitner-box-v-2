from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

import psycopg2
from . import models, schemas, utils
from .database import engine, get_db
from .routers import card, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(card.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Leitner Box"}


