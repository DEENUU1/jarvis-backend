from fastapi import APIRouter
from ai.integration import google_calendar

router = APIRouter(
    prefix="",
    tags=["health"],
)


@router.get("/health", tags=["health"])
def health():
    return {"status": "okk"}


@router.get("/test")
def test():
    calendar = google_calendar.Calendar()
    calendar_event = calendar.get_all_events()
    print(calendar_event)