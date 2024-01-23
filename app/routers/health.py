from fastapi import APIRouter
from ai.integration.google_calendar import Calendar


router = APIRouter(
    prefix="",
    tags=["health"],
)


@router.get("/health", tags=["health"])
def health():
    return {"status": "okk"}


@router.get("/calendar", tags=["calendar"])
def calendar():
    c = Calendar()
    c.get_all_events()

    return {"status": "okk"}