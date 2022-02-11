from enum import Enum
from typing import List

import databases

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, func


# Initialize api
app = FastAPI()

# Define openAPI spec


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Draft Game API",
        version="0.1.0",
        description="API for Draft Game Card Assets",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

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
    """Draft Game API Home Page"""
    return {"message": "Welcome to Draft Game API"}


@app.get("/cards/", response_model=List[Card])
async def get_cards(
    card_name: str = None,
    card_type: CardType = None,
    effect: str = None,
    limit: int = 100,
):
    """
    Get list of Cards
    """
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
    """Get single card by name"""
    query = cards.select().where(cards.c.name == card_name)
    results = await database.fetch_one(query=query)
    return results


@app.get("/random-cards/", response_model=List[Card])
async def get_random_cards(limit: int = 1):
    """Get random list of cards. Configurable limit"""
    query = cards.select().order_by(func.random()).limit(limit)
    results = await database.fetch_all(query=query)
    return results
