from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import card, user, auth
from .config import settings

 # using sqlalchemy to initialize tables
from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [settings.front_end_url
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(card.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Leitner Box"}
