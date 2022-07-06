from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    username: str

class UserOut(BaseModel):
    user_id: int
    email: str
    username: str
    current_day_number: int = 1
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    current_day_number: Optional[int] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class CardBase(BaseModel):
    subject: Optional[str] = None
    question: str
    answer: str
    level: int = 1
    is_active: bool = True

class CardOut(CardBase):
    card_id: int
    creator_id: int
   

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class TestCard(BaseModel):
    card_id: int
    question: str 
