from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_cards = [{"subject": "Spanish", "question": "comer", "answer": "to eat", "active": True, "id": 1},
{"subject": "Spanish", "question": "haber", "answer": "to speak", "active": True, "id": 2}]

class Card(BaseModel):
    subject: str
    question: str
    answer: str
    active: bool = True

@app.get("/")
async def root():
    return {"message": "Welcome to Leitner Box"}

@app.get('/cards')
def get_cards():
    return {"data": my_cards}

@app.post("/cards")
def create_card(card: Card):
    card_dict = card.dict()
    card_dict['id'] = randrange(0, 1000000)
    my_cards.append(card_dict)
    return{"data": card_dict}