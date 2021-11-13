from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_cards = [{"subject": "Spanish", "question": "comer", "answer": "to eat", "active": True, "id": 1},
{"subject": "Spanish", "question": "haber", "answer": "to speak", "active": True, "id": 2}]

def find_card(id):
    for c in my_cards:
        if c["id"] == id:
            return c

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

@app.get('/cards/{id}')
def get_card(id:int, response: Response):
    card = find_card(id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} was not found")
    return {"card": card}
