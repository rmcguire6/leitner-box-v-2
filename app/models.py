from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Card(Base):
  __tablename__ = 'cards'

  card_id = Column(Integer, primary_key=True)
  subject = Column(String(64), nullable=False)
  question = Column(String(120), nullable=False)
  answer = Column(String(120), nullable=False)
  is_active = Column(Boolean, server_default='TRUE', nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
