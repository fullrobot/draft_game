from enum import Enum
from typing import List

import databases

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, func


# Initialize api
app = FastAPI()

# Define Types
class Card(BaseModel):
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


# Initialize Database
DATABASE_URL = "sqlite:///./app/cards.db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

cards = Table(
    "cards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("value", Integer),
    Column("card_type", String),
    Column("effect", String),
)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Welcome to Draft Game API"}


@app.get("/cards/", response_model=List[Card])
async def get_cards(
    card_name: str = None,
    card_type: CardType = None,
    effect: str = None,
    limit: int = 100,
):
    query = cards.select()
    if card_name:
        query = query.where(cards.c.name == card_name)
    if card_type:
        query = query.where(cards.c.card_type == card_type)
    if effect:
        query = query.where(cards.c.effect.like(f"%{effect}%"))
    results = await database.fetch_all(query=query)
    return results[:limit]


@app.get("/cards/{card_name}/", response_model=Card)
async def get_card(card_name: str):
    query = cards.select().where(cards.c.name == card_name)
    results = await database.fetch_one(query=query)
    return results


@app.get("/random-cards/", response_model=List[Card])
async def get_random_cards(limit: int = 1):
    query = cards.select().order_by(func.random()).limit(limit)
    results = await database.fetch_all(query=query)
    return results
