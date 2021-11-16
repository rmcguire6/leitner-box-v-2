from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Card(Base):
  __tablename__ = 'cards'

  card_id = Column(Integer, primary_key=True)
  subject = Column(String(64), nullable=False)
  question = Column(String(120), nullable=False)
  answer = Column(String(120), nullable=False)
  is_active = Column(Boolean, default=True)
