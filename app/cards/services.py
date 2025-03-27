from sqlalchemy.orm import Session
from app.cards.models import Card, Effect


def get_cards(db: Session) -> list[Card]:
    cards = db.query(Card).join(Card.effect).all()
    return [card.serialize for card in cards]


def get_card_by_id(db: Session, card_id: int) -> Card:
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        card.effect = db.query(Effect).filter(Effect.id == card.effect_id).first()
    return card.serialize


def create_card(db: Session, card: Card) -> Card:
    db_card = Card(name=card.name, card_type=card.card_type, value=card.value)
    db.add(db_card)
    db.commit()
    return db_card
