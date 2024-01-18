import shutil

from fastapi import APIRouter
from fastapi import File, UploadFile


router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post("/upload")
def upload_file(uploaded_file: UploadFile = File(...)):
    path = f"media/{uploaded_file.filename}"

    with open(path, "w+b") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return {
        "filename": uploaded_file.filename,
        "path": path
    }