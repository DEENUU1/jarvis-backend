from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=["health"],
)


@router.get("/health", tags=["health"])
def health():
    return {"status": "okk"}
