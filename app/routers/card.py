from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)

@router.get('/', response_model=List[schemas.CardOut])
def get_cards(db: Session= Depends(get_db)):
    cards = db.query(models.Card).all()
    return cards

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.CardOut)
def create_card(card: schemas.CardBase, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print('user_id is ', user_id)
    new_card = models.Card(**card.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.get('/{id}', response_model=schemas.CardOut)
def get_card(id:int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == id).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} was not found")
    return card

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_card(id:int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    card_query = db.query(models.Card).filter(models.Card.card_id == id)
    if card_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    card_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.CardOut)
def update_card(id:int, card: schemas.CardBase,  db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    card_query = db.query(models.Card).filter(models.Card.card_id == id)
    found_card = card_query.first()
    if found_card == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with id {id} does not exist")
    card_query.update(card.dict(), synchronize_session=False)
    db.commit()
    return card_query.first()
