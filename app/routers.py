from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine
from .schemas import CardBase, CardType

models.Base.metadata.create_all(bind=engine)
cardrouter = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@cardrouter.get("/cards/", response_model=List[CardBase])
def get_cards(
    skip: int = 0,
    limit: int = 100,
    card_name: str = None,
    card_type: CardType = None,
    effect: str = None,
    session: Session = Depends(get_session),
):
    items = crud.get_cards(
        session=session,
        skip=skip,
        limit=limit,
        card_name=card_name,
        card_type=card_type,
        effect=effect,
    )
    return [i.serialize for i in items]


@cardrouter.get("/cards/{name}", response_model=CardBase)
def get_card(
    name: str,
    session: Session = Depends(get_session),
):
    card = crud.get_card_by_name(session=session, name=name)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card.serialize
