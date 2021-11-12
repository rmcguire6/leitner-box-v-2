from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Card(BaseModel):
    subject: str
    question: str
    answer: str
    active: bool = True

@app.get("/")
async def root():
    return {"message": "Welcome to Leitner Box"}

@app.post("/cards")
def create_card(card: Card):
    print(card.dict())
    return{"data":"card"}