from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cards.models import Card
from app.cards.schemas import CardSchema
from app.database import get_db
from app.cards import services

router = APIRouter()


@router.get("/cards", response_model=list[CardSchema])
def get_cards(db: Annotated[Session, Depends(get_db)]):
    return services.get_cards(db)


@router.get("/cards/{card_id}", response_model=CardSchema)
def get_card(card_id: int, db: Annotated[Session, Depends(get_db)]):
    return services.get_card_by_id(db, card_id)


@router.post("/cards", response_model=CardSchema)
def create_card(card: CardSchema, db: Annotated[Session, Depends(get_db)]):
    return services.create_card(db, card)
