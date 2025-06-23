from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.api.v1.router import router as v1_router
from app.database.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  # Initializes tables (SQLAlchemy)
    print("✅ Application started and database tables created!")
    yield
    print("🛑 Application shutting down!")


app = FastAPI(
    title="Draft Game API",
    description="API for managing a card draft game",
    version="0.1.0",
    docs_url="/api",
    lifespan=lifespan,
)

api_root_router = APIRouter(prefix="/api")
api_root_router.include_router(v1_router)
app.include_router(api_root_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
