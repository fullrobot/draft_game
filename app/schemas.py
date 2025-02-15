from enum import Enum

from pydantic import BaseModel


class CardBase(BaseModel):
    id: int
    name: str
    value: int
    card_type: str
    effect: str


class CardType(str, Enum):
    wizard = "Wizard"
    peasant = "Peasant"
    royal = "Royal"
    pirate = "Pirate"


class CreateCard(BaseModel):
    name: str
    value: int
    card_type: CardType
    effect: str
