from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Users"]
)

@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email_query = db.query(models.User).filter(models.User.email == user.email).first()
    if email_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not unique. Did you mean to login?")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}/", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    return user