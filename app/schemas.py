from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    cards_per_day: int

class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    cards_per_day: int
    current_day_number: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CardBase(BaseModel):
    subject: str
    question: str
    answer: str
    is_active: bool = True


class CardOut(CardBase):
    created_at: datetime
    card_id: int
    creator_id: int
    level: int
    creator: UserOut

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
