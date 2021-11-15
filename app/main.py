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

def find_index_card(id):
    for index, c in enumerate(my_cards):
        if c['id'] == id:
            return index

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

@app.post("/cards", status_code=status.HTTP_201_CREATED)
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