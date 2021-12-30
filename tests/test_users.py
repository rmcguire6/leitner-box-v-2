import pytest
from app import schemas
from jose import jwt
from app.config import settings

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
  login_res = schemas.Token(**res.json())
  payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
  id = payload.get("user_id")
  print(res.json())
  assert id == test_user['user_id']
  assert login_res.token_type == 'bearer'
  assert res.status_code == 200

