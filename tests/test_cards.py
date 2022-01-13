from typing import List
from app import schemas
import pytest

def test_get_all_cards(authorized_client, test_cards):
  res = authorized_client.get("/cards/")

  def validate(card):
    return schemas.CardOut(**card)
  cards_map = map(validate, res.json())
  cards_list = list(cards_map)

  assert res.status_code == 200
  assert cards_list[0].card_id == test_cards[0].card_id

def test_unauthorized_user_get_all_cards(client, test_cards):
  res = client.get("/cards/")
  assert res.status_code == 401

def test_get_one_card(authorized_client, test_cards):
  res = authorized_client.get(f"/cards/{test_cards[0].card_id}")
  card = schemas.CardOut(**res.json())
  assert card.card_id == test_cards[0].card_id
  assert card.subject == test_cards[0].subject
  assert card.question == test_cards[0].question
  assert card.answer == test_cards[0].answer
  assert card.is_active == test_cards[0].is_active
  assert card.creator_id == test_cards[0].creator_id
  assert card.level == test_cards[0].level
  assert res.status_code == 200

def test_unauthorized_user_get_one_card(client, test_cards):
  res = client.get(f"/cards/{test_cards[0].card_id}")
  assert res.status_code == 401

def test_get_one_card_that_does_not_exist(authorized_client, test_cards):
  res = authorized_client.get("/cards/-9")
  assert res.status_code == 404

@pytest.mark.parametrize("subject, question, answer",
[("Geography", "How many continents are there?", "7"),
("Geography", "How many oceans are there?", "5"),
("Geography", "How many poles are there?", "2"),
("Geography", "How many distinct colors are needed to color any map with no colors next to each other?", "4"),])
def test_create_card(authorized_client, test_user, subject, question, answer):
  res = authorized_client.post("/cards/", json={"subject": subject, "question": question, "answer": answer})
  created_card = schemas.CardOut(**res.json())
  assert res.status_code == 201
  assert created_card.subject == subject
  assert created_card.question == question
  assert created_card.answer == answer
  assert created_card.creator_id == test_user['user_id']

def test_create_card_default_is_active_true(authorized_client, test_user):
  res = authorized_client.post("/cards/", json={"subject": "Spanish", "question": "pelota", "answer": "ball"})
  created_card = schemas.CardOut(**res.json())
  assert created_card.subject == "Spanish"
  assert created_card.question == "pelota"
  assert created_card.answer == "ball"
  assert created_card.creator_id == test_user['user_id']
  assert res.status_code == 201
  assert created_card.is_active == True

def test_unauthorized_user_create_card(client):
  res = client.post("/cards/", json={"subject": "Spanish", "question": "pelota", "answer": "ball"})
  assert res.status_code == 401

def test_authorized_user_delete_card(authorized_client, test_cards):
  res = authorized_client.delete(f"/cards/{test_cards[0].card_id}")
  assert res.status_code == 204

def test_unauthorized_user_delete_card(client, test_cards):
  res = client.delete(f"/cards/{test_cards[0].card_id}")
  assert res.status_code == 401

def test_delete_non_existant_card(authorized_client, test_cards):
  res = authorized_client.delete(f"/cards/-99")
  assert res.status_code == 404

def test_delete_other_user_card(authorized_client, test_cards):
  res = authorized_client.delete(f"/cards/{test_cards[3].card_id}")
  assert res.status_code == 403
  