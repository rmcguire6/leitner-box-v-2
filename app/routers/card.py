from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Cards"]
)

@router.get('/cards/', response_model=List[schemas.CardOut])
def get_all_users_cards(db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    cards = db.query(models.Card).filter(models.Card.creator_id == current_user.user_id).all()
    return cards

@router.post("/cards/", status_code=status.HTTP_201_CREATED, response_model= schemas.CardOut)
def create_card(card: schemas.CardBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_card = models.Card(**card.dict())
    new_card.creator_id = current_user.user_id
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.get('/cards/{id}', response_model=schemas.CardOut)
def get_card(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    card = db.query(models.Card).filter(models.Card.card_id == id).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} was not found")
    return card

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_card(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    card_query = db.query(models.Card).filter(models.Card.card_id == id)
    card = card_query.first()
    if card == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    if card.creator_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    card_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.CardOut)
def update_card(id:int, card: schemas.CardBase,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    card_query = db.query(models.Card).filter(models.Card.card_id == id)
    found_card = card_query.first()
    if found_card == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with id {id} does not exist")
    if found_card.creator_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    card_query.update(card.dict(), synchronize_session=False)
    db.commit()
    return card_query.first()
