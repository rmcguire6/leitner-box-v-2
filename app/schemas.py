from pydantic import BaseModel, EmailStr
from datetime import datetime

class CardBase(BaseModel):
    subject: str
    question: str
    answer: str
    is_active: bool = True


class CardOut(CardBase):
  created_at: datetime
  card_id: int

  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str
  username: str
  cards_per_day: int
