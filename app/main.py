from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.cards.router import router as cardrouter
from app.database import engine
from app.models import Base

# Initialize api
app = FastAPI()
app.include_router(cardrouter)

# Create tables
Base.metadata.create_all(bind=engine)


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


@app.get("/")
async def read_root():
    return {"Hello": "World"}
