from typing import TypedDict

from slugify import slugify
from sqlalchemy import Column, Integer, String

from .database import Base


class CardDict(TypedDict):
    id: int
    name: str
    value: int
    card_type: str
    effect: str


class Card(Base):
    """
    Defines Card model
    """

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    value = Column(Integer)
    card_type = Column(String(50))
    effect = Column(String(500))
    slug = Column(String(50))

    def __init__(self, name: str, value: int, card_type: str, effect: str, slug: str):
        self.name = name
        self.value = value
        self.card_type = card_type
        self.effect = effect
        self.slug = slugify(name)

    def __repr__(self) -> str:
        return self.name

    @property
    def serialize(self) -> CardDict:
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "card_type": self.card_type,
            "effect": self.effect,
        }
