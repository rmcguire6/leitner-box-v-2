from pydantic import BaseModel
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