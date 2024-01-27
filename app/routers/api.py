from fastapi import APIRouter
from .v1 import chat, health, media


router = APIRouter(prefix="/api/v1")

router.include_router(health.router)
router.include_router(media.router)
router.include_router(chat.router)
