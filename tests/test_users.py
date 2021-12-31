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

@pytest.mark.parametrize("email, password, status_code", [
  ('wrongemail@example.com', '123pass', 403),
  ('abby@example.com', 'wrongpassword', 403),
  ('wrongemail@example.com', 'wrongpassword', 403),
  (None, '123pass', 422),
  ('abby@example.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
  res = client.post("/login/", data={
    "username": email,
    "password": password
  })
  assert res.status_code == status_code


def test_get_user_by_id(test_user, client):
  res = client.get("/users/1/")
  found_user = schemas.UserOut(**res.json())
  assert res.status_code == 200
  assert found_user.user_id == test_user['user_id']
  assert found_user.email == test_user['email']
  assert found_user.username == test_user['username']
  assert found_user.cards_per_day == test_user['cards_per_day']
  assert found_user.current_day_number == test_user['current_day_number']

def test_incorrect_user_id(test_user, client):
  res = client.get("/users/-5")
  assert res.status_code == 404