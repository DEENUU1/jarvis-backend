from typing import Dict

from fastapi import APIRouter, status

router = APIRouter(
    prefix="",
    tags=["health"],
)


@router.get(
    "/",
    summary="Health check",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK
)
def health():
    return {"status": "ok"}
