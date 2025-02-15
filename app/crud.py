from typing import List

from sqlalchemy.orm import Session

from .models import Card
from .schemas import CardType


def get_card_by_name(session: Session, name: str) -> Card:
    return session.query(Card).filter(Card.slug == name).first()


def get_cards(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    card_name: str = None,
    card_type: CardType = None,
    effect: str = None,
) -> List[Card]:

    filters = []
    if card_name:
        filters.append(Card.name == card_name)
    if card_type:
        filters.append(Card.card_type == card_type)
    if effect:
        filters.append(Card.effect.like(f"%{effect}%"))

    return session.query(Card).filter(*filters).offset(skip).limit(limit).all()
