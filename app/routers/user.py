from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db


router = APIRouter(
    tags=["Users"]
)


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email_query = db.query(models.User).filter(
        models.User.email == user.email).first()
    if email_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not unique. Did you mean to login?")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}/", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} was not found")
    return user

@router.put("/users/{user_id}/", response_model=schemas.UserOut)
def update_user(user_id: int, updatedUser: schemas.UserUpdate, db: Session = Depends(get_db), ):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    db_user = user_query.first()
    if not updatedUser.username:
        updatedUser.username = db_user.username
    if not updatedUser.email:
        updatedUser.email = db_user.email
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} was not found")
    user_query.update(updatedUser.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()
