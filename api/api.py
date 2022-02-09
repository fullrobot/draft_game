import databases
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize api
app = FastAPI()

# Initialize Database
DATABASE_URL = "sqlite:///./assets/cards.db"
database = databases.Database(DATABASE_URL)

# Define Types
class Card(BaseModel):
    id: int
    name: str
    value: int
    type: str
    effect: str


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"messagew": "Welcome to Draft Game API"}


@app.get("/cards/", response_model=List[Card])
async def get_cards(limit: int = 10):
    query = f"SELECT * FROM cards;"
    results = await database.fetch_all(query=query)
    return results[:limit]


@app.get("/cards/{card_id}/", response_model=Card)
async def get_card(card_id: int):
    query = f"SELECT * FROM cards WHERE id={card_id};"
    results = await database.fetch_one(query=query)
    return results
