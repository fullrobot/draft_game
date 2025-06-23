import enum
from typing import Optional, TypedDict

from slugify import slugify
from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.init_db import Base


class EffectType(str, enum.Enum):
    TIMING = "timing"
    DELAYED = "delayed"
    CONDITIONAL = "conditional"
    ONGOING = "ongoing"
    GAME_RULE = "game_rule"
    STEAL = "steal"
    COUNTER = "counter"
    SWAP = "swap"
    DRAFT_MANIPULATION = "draft_manipulation"


class EffectDict(TypedDict):
    id: int
    description: str
    effect_type: str
    value_change: int
    condition: str
    game_effect: str


class CardDict(TypedDict):
    id: int
    name: str
    value: int
    card_type: str
    effect: EffectDict


class Effect(Base):
    __tablename__ = "effects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    description: Mapped[str]
    effect_type: Mapped[EffectType] = mapped_column(Enum(EffectType, native_enum=False))
    value_change: Mapped[int] = mapped_column(nullable=True)
    condition: Mapped[str] = mapped_column(nullable=True)
    game_effect: Mapped[str] = mapped_column(nullable=True)

    @property
    def serialize(self) -> EffectDict:
        return {
            "id": self.id,
            "description": self.description,
            "effect_type": self.effect_type.value,
            "value_change": self.value_change,
            "condition": self.condition,
            "game_effect": self.game_effect,
        }


class Card(Base):
    """
    Defines Card model
    """

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    slug: Mapped[str] = mapped_column(index=True)
    value: Mapped[int]
    card_type: Mapped[str]
    effect_id: Mapped[int] = mapped_column(ForeignKey("effects.id"))
    effect_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("effects.id"))

    # Define the relationship
    effect: Mapped[Optional[Effect]] = relationship("Effect", lazy="joined")

    def __init__(
        self,
        name: str,
        value: int,
        card_type: str,
        effect: Effect,
    ) -> None:
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
