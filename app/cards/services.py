from sqlalchemy.orm import Session

from app.cards.filter import CardFilter
from app.cards.models import Card, Effect
from app.cards.schemas import CreateCard


async def get_cards(db: Session, filter: CardFilter) -> list[Card]:
    cards = (
        db.query(Card)
        .join(Card.effect)
        .order_by(filter.order_by)
        .offset(filter.offset)
        .limit(filter.limit)
        .all()
    )
    return [card.serialize for card in cards]


def get_card_by_id(db: Session, card_id: int) -> Card:
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        card.effect = db.query(Effect).filter(Effect.id == card.effect_id).first()
        return card.serialize


def create_card(db: Session, card: CreateCard) -> Card:
    card = CreateCard.model_validate(card)
    effect = Effect(**card.effect.model_dump())
    db.add(effect)
    db.commit()
    db.refresh(effect)
    card = Card(
        name=card.name,
        value=card.value,
        card_type=card.card_type,
        effect=effect,
    )
    db.add(card)
    db.commit()
    return card.serialize
