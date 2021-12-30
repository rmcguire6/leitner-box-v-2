from fastapi.testclient import TestClient
import pytest 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(
  SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
      yield db 
       
    finally:
      db.close()
        
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  yield TestClient(app)
  

def test_root(client):
  res = client.get("/")
  print(res.json().get("message"))
  assert res.json().get("message") == 'Welcome to Leitner Box'

def test_create_user(client):
  res = client.post("/users/", json={
    "email": "abby@example.com",
    "username": "Abby",
    "cards_per_day": 3,
    "password": "123pass"
    })
  print(res.json())
  assert res.json().get("email") == "abby@example.com"
  assert res.status_code == 201