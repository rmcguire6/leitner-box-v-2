from typing import List
from sqlalchemy.orm import Session
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from ..import models, schemas, oauth2
from ..database import get_db



router = APIRouter(
    tags=["Cards"]
)


@router.get('/cards/', response_model=List[schemas.CardOut])
def get_all_users_cards(db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    cards = db.query(models.Card).filter(models.Card.creator_id == current_user.user_id).all()
    return cards


@router.post("/cards/", status_code=status.HTTP_201_CREATED, response_model=schemas.CardOut)
def create_card(card: schemas.CardBase, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    new_card = models.Card(**card.dict())
    new_card.creator_id = current_user.user_id
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.get('/cards/{card_id}', response_model=schemas.CardOut)
def get_card(card_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"card with id {card_id} was not found")
    return card

@router.delete('/cards/{card_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    card_query = db.query(models.Card).filter(models.Card.card_id == card_id)
    if card_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    if card_query.first().creator_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    card_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/cards/{card_id}', response_model=schemas.CardOut)
def update_card(card_id:int, card: schemas.CardBase,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    card_query = db.query(models.Card).filter(models.Card.card_id == card_id)
    found_card = card_query.first()
    if found_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card with id {id} does not exist")
    if found_card.creator_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    card_query.update(card.dict(), synchronize_session=False)
    db.commit()
    return card_query.first()
front_end_cards = [{
    "card_id": 1,
    "answer": 'to live',
    "question": "vivir",
}, {
    "card_id": 2,
    "answer": "to drink",
    "question": "tomar",
}, {
    "card_id": 3,
    "answer": "to eat",
    "question": "comer",
}, {
    "card_id": 4,
    "answer": "to write",
    "question": "escribir",
}]
@router.get('/test_cards/')
def get_test_cards():
    return front_end_cards

@router.post('/test_cards/', status_code=status.HTTP_201_CREATED)
def create_new_test_card(card: dict = Body(...)):
    front_end_cards.append(card)
    print(front_end_cards)
    return card
