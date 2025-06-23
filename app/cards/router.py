from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.cards import services
from app.cards.filter import CardFilter
from app.cards.schemas import CardSchema, CreateCard
from app.database.init_db import get_db

router = APIRouter()


@router.get("/cards", response_model=list[CardSchema])
async def get_cards(filter: Annotated[CardFilter, Query()], db: Annotated[Session, Depends(get_db)]):
    return await services.get_cards(db, filter)


@router.get("/cards/{card_id}", response_model=CardSchema)
def get_card(card_id: int, db: Annotated[Session, Depends(get_db)]):
    return services.get_card_by_id(db, card_id)


@router.post("/cards", response_model=CardSchema)
def create_card(card: CreateCard, db: Annotated[Session, Depends(get_db)]):
    return services.create_card(db, card)
