import pytest
from app import schemas
from .database import client, session

def test_root(client):
  res = client.get("/")
  print(res.json().get("message"))
  assert res.json().get("message") == 'Welcome to Leitner Box'

@pytest.fixture
def test_user(client):
  user_data = {
    "email": "abby@example.com",
    "username": "Abby",
    "cards_per_day": 3,
    "password": "123pass"
    }
  res = client.post("/users/", json=user_data)
  print(res.json())
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_data['password']
  print('new_user', new_user)
  return new_user


def test_create_user(client):
  res = client.post("/users/", json={
    "email": "abby@example.com",
    "username": "Abby",
    "cards_per_day": 3,
    "password": "123pass"
    })
  new_user = schemas.UserOut(**res.json())
  assert new_user.email == 'abby@example.com'
  assert res.status_code == 201

def test_login_user(client, test_user):
  res = client.post("/login/", data={
    "username": test_user['email'],
    "password": test_user['password']
    })
  print(res.json())
  assert res.status_code == 200

