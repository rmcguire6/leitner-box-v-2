from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


my_cards = [{"subject": "Spanish", "question": "comer", "answer": "to eat", "active": True, "id": 1},
{"subject": "Spanish", "question": "haber", "answer": "to speak", "active": True, "id": 2}]

def find_card(id):
    for c in my_cards:
        if c["id"] == id:
            return c

def find_index_card(id):
    for index, c in enumerate(my_cards):
        if c['id'] == id:
            return index

class Card(BaseModel):
    subject: str
    question: str
    answer: str
    is_active: bool = True

@app.get("/")
async def root():
    return {"message": "Welcome to Leitner Box"}


@app.get('/cards')
def get_cards(db: Session= Depends(get_db)):
    cards = db.query(models.Card).all()
    return {"data": cards}

@app.post("/cards", status_code=status.HTTP_201_CREATED)
def create_card(card: Card, db: Session= Depends(get_db)):
    new_card = models.Card(**card.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return{"data": new_card}

@app.get('/cards/{id}')
def get_card(id:int, response: Response):
    card = find_card(id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} was not found")
    return {"card": card}

@app.delete('/cards/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_card(id:int):
    index = find_index_card(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    my_cards.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/cards/{id}')
def update_card(id:int, card: Card):
    index = find_index_card(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    card_dict = card.dict()
    card_dict['id'] = id
    my_cards[index] = card_dict
    return {'message': 'Updated card'}