from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import card, user, auth

app = FastAPI()
origins = ["http://localhost:3000",
           "localhost:3000"
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
