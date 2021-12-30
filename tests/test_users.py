import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
  res = client.get("/")
  assert res.json().get("message") == 'Welcome to Leitner Box'



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
  assert id == test_user['user_id']
  assert login_res.token_type == 'bearer'
  assert res.status_code == 200

def test_incorrect_login(test_user, client):
  res = client.post("/login/", data={
    "username":test_user['email'],
    "password":"wrong password"
  })
  assert res.status_code == 403
  assert res.json().get('detail') == 'Invalid Credentials'