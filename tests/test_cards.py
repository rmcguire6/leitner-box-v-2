from typing import List
from app import schemas

def test_get_all_cards(authorized_client, test_cards):
  res = authorized_client.get("/cards/")

  def validate(card):
    return schemas.CardOut(**card)
  cards_map = map(validate, res.json())
  cards_list = list(cards_map)

  assert len(res.json()) == len(test_cards)
  assert res.status_code == 200
  assert cards_list[0].card_id == test_cards[0].card_id
