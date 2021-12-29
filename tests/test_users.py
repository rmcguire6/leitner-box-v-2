from fastapi import FastAPI
from fastapi.testclient import TestClient 
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
  res = client.get("/")
  print(res.json().get("message"))
  assert res.json().get("message") == 'Welcome to Leitner Box'

def test_create_user():
  res = client.post("/users/", json={
    "email": "abby@example.com",
    "username": "Abby",
    "cards_per_day": 3,
    "password": "123pass"
    })
  print(res.json())
  assert res.json().get("email") == "abby@example.com"
  assert res.status_code == 201