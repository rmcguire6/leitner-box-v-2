from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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
  creator_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False )
  creator = relationship("User")

class User(Base):
  __tablename__ = 'users'
  user_id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  cards_per_day = Column(Integer, nullable=False, default=5)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))