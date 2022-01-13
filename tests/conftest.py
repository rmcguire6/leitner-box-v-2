from fastapi.testclient import TestClient
import pytest 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(
  SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db 
    
  finally:
    db.close()

@pytest.fixture
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)

@pytest.fixture
def test_user(client):
  user_data = {
    "email": "abby@example.com",
    "username": "Abby",
    "cards_per_day": 3,
    "password": "123pass"
    }
  res = client.post("/users/", json=user_data)
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_data['password']
  return new_user

@pytest.fixture
def test_user2(client):
  user_data = {
    "email": "burt@example.com",
    "username": "Burt",
    "cards_per_day": 5,
    "password": "123pass"
    }
  res = client.post("/users/", json=user_data)
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_data['password']
  return new_user

@pytest.fixture
def token(test_user):
  return create_access_token({"user_id": test_user['user_id']})

@pytest.fixture
def authorized_client(client, token):
  client.headers = {
    **client.headers,
    "Authorization": f"Bearer {token}"
  }
  return client

@pytest.fixture
def test_cards(test_user, test_user2, session):
  cards_data = [{
    "subject": "Spanish",
    "question": "vivir",
    "answer" : "to live",
    "creator_id": test_user['user_id'],
    "is_active": True
  }, {
    "subject": "Spanish",
    "question": "tomar",
    "answer" : "to take",
    "creator_id": test_user['user_id'],
    "is_active": True
  },{
    "subject": "Spanish",
    "question": "comer",
    "answer" : "to eat",
    "creator_id": test_user['user_id'],
    "is_active": True
  },{
    "subject": "Spanish",
    "question": "escribir",
    "answer" : "to write",
    "creator_id": test_user2['user_id'],
    "is_active": True
  }]

  def create_card_model(card):
    return models.Card(**card)

  card_map = map(create_card_model, cards_data)
  cards = list(card_map)

  session.add_all(cards)
  session.commit()

  db_cards = session.query(models.Card).all()
  return db_cards

