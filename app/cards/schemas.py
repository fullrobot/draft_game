from enum import Enum

from pydantic import BaseModel


class EffectType(str, Enum):
    TIMING = "timing"
    DELAYED = "delayed"
    CONDITIONAL = "conditional"
    ONGOING = "ongoing"
    GAME_RULE = "game_rule"
    STEAL = "steal"
    COUNTER = "counter"
    SWAP = "swap"
    DRAFT_MANIPULATION = "draft_manipulation"


class CardType(str, Enum):
    wizard = "Wizard"
    peasant = "Peasant"
    royal = "Royal"
    pirate = "Pirate"


class EffectSchema(BaseModel):
    id: int
    description: str
    effect_type: EffectType
    value_change: int
    condition: str
    game_effect: str


class CardSchema(BaseModel):
    id: int
    name: str
    value: int
    card_type: CardType
    effect: EffectSchema


class CreateCard(BaseModel):
    name: str
    value: int
    card_type: CardType
    effect: EffectSchema
