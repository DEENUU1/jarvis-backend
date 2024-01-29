import os
import shutil
from typing import Dict, Any

from fastapi import APIRouter, Depends, File, UploadFile, Response, status, BackgroundTasks
from sqlalchemy.orm import Session

from ai.vector import save_to_pinecone
from ai.vector import split_files
from config.database import get_db
from tasks.media import chat_history_embedding_task, fetch_notion_task, notion_embedding_task

router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post(
    "/file",
    summary="Upload file",
    status_code=status.HTTP_201_CREATED,
)
def upload_file(uploaded_file: UploadFile = File(...)) -> Dict[str, str] | Any:
    """
    Endpoint for uploading a file, processing its content, and saving it to Pinecone.
    """
    path = f"media/{uploaded_file.filename}"

    available_files = [".pdf", ".csv", ".json", ".md", ".txt"]
    if not uploaded_file.filename.endswith(tuple(available_files)):
        return Response(content="Invalid file type", status_code=400)

    with open(path, "w+b") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    chunks = split_files(path)
    save_to_pinecone(chunks)
    os.remove(path)

    return {"message": "File uploaded successfully"}


@router.post(
    "/chat",
    summary="Embedding chat",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, str]
)
def run_embedding_chat(background_task: BackgroundTasks) -> Dict[str, str]:
    """
    Load all conversations and messages, split into chunks and load to pinecone vector db
    """
    background_task.add_task(chat_history_embedding_task)

    return {"message": "Embedding chat"}


@router.post(
    "/notion",
    summary="Update Notion data",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, str],
)
def run_notion(background_task: BackgroundTasks, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Endpoint to load and update data from Notion to SQLite
    """
    background_task.add_task(fetch_notion_task, db)

    return {"message": "Notion data updated"}


@router.post(
    "/notion/embedding",
    summary="Update Notion data",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, str]
)
def run_notion_embedding(background_task: BackgroundTasks, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Endpoint to load and update data from Notion to SQLite
    """
    background_task.add_task(notion_embedding_task, db)

    return {"message": "Notion data updated"}
