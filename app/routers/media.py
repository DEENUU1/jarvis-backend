import os
import shutil

from fastapi import APIRouter
from fastapi import File, UploadFile

from ai.vector import split_files
from ai.vector import save_to_pinecone

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

    # Get all files from root path
    pdf_files = [f for f in os.listdir(root_path)]

    for file in pdf_files:
        # Get path for file
        file_path = os.path.join(root_path, file)
        # Run function to split files into chunks and return it
        chunks = split_files(file_path)
        # Save chunks to pinecone vector database
        save_to_pinecone(chunks)

        # Delete file after processing
        os.remove(file_path)


