from pydantic import BaseModel

class Card(BaseModel):
    subject: str
    question: str
    answer: str
    is_active: bool = True
