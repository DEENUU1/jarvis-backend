import shutil

from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi import Response

from ai.integration.notion import notion, get_map_category
from ai.sql_chat_history import get_all_conversations
from ai.vector import save_to_pinecone
from ai.vector import split_files
from config.settings import settings
from schemas.media import FileCategory

import os

router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post("/file")
def upload_file(file_category: FileCategory, uploaded_file: UploadFile = File(...)):
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
    save_to_pinecone(chunks, file_category.name)
    os.remove(path)

    return {"message": "Embedding completed"}


@router.post("/chat")
def run_embedding_chat():
    """
    Load all conversations and messages, split into chunks and load to pinecone vector db
    """
    conversations = get_all_conversations()
    for conversation in conversations:
        chunks = split_files(data=conversation)
        save_to_pinecone(chunks, settings.PINECONE_PRIVATE_INDEX)

    return {"message": "Embedding completed"}


@router.post("/notion")
def run_embedding_notion():
    """
    Endpoint to load all databases into vector db
    """
    mapper = get_map_category()
    for category in mapper.keys():
        for dbs in mapper[category]:
            parsed_pages = notion(
                category=category,
                dbs=dbs
            )
            for content in parsed_pages:
                if content:
                    chunks = split_files(data=content)
                    save_to_pinecone(chunks, category.value)

    return {"message": "Embedding completed"}
