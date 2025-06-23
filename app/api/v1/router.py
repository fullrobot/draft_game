from fastapi import APIRouter

from app.cards.router import router as cardrouter


router = APIRouter(prefix="/v1")
router.include_router(cardrouter, tags=["cards"])
