import os
import shutil

from fastapi import APIRouter
from fastapi import File, UploadFile

from ai.pdf import split_pdf
from ai.vector import save_to_chroma_db

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


@router.post("/embedding")
def run_embedding():
    root_path = "media"

    # Get all PDF files
    pdf_files = [f for f in os.listdir(root_path) if f.endswith(".pdf")]

    for file in pdf_files:
        # Get path for file
        file_path = os.path.join(root_path, file)
        # Run function to split PDF into chunks and return it
        chunks = split_pdf(file_path)
        # Save chunks to chromadb
        save_to_chroma_db(chunks)

        # Delete file after processing
        os.remove(file_path)


