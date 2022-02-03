from typing import List
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..import models, schemas, oauth2, front_end_data
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

@router.get('/test_cards/')
def get_test_cards():
    res = front_end_data.front_cards()
    return res
@router.post('/test_cards/', status_code=status.HTTP_201_CREATED)
def create_test_question(card=front_end_data.front_test_card()):
    res = front_end_data.front_cards()
    res.append(card)
    return card
