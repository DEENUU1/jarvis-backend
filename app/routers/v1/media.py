import os
import shutil

from fastapi import APIRouter, Depends, File, UploadFile, Response, status
from config.database import get_db
from services.chat import get_all_conversations
from ai.vector import save_to_pinecone
from ai.vector import split_files
from config.settings import settings
from integration.notion import notion
from services import notion as ns
from sqlalchemy.orm import Session
from schemas.notion import NotionCreateSchema, NotionUpdateSchema
from datetime import timezone


router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post(
    "/file",
    summary="Upload file",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
def upload_file(uploaded_file: UploadFile = File(...)):
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

    return Response(content="File uploaded and processed", status_code=201)


@router.post(
    "/chat",
    summary="Embedding chat",
    status_code=status.HTTP_201_CREATED,
    response_class=Response
)
def run_embedding_chat() -> Response:
    """
    Load all conversations and messages, split into chunks and load to pinecone vector db
    """
    conversations = get_all_conversations()
    for conversation in conversations:
        chunks = split_files(data=conversation)
        save_to_pinecone(chunks)

    return Response(content="Embedding completed", status_code=201)


@router.post(
    "/notion",
    summary="Update Notion data",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
def run_notion(db: Session = Depends(get_db)) -> Response:
    """
    Endpoint to load and update data from Notion to SQLite
    """
    for dbs in settings.NOTION_DATABASES:
        parsed_pages = notion(dbs=dbs)
        for page in parsed_pages:
            if page:
                if ns.notion_object_exist(db, page_id=page.page_id):
                    existing_object = ns.get_notion_object_by_page_id(db, page_id=page.page_id)
                    existing_object_updated_at = existing_object.updated_at.replace(tzinfo=timezone.utc)

                    if existing_object_updated_at < page.updated_at:
                        ns.update_notion_content(
                            session=db,
                            page_id=page.page_id,
                            data=NotionUpdateSchema(
                                updated_at=page.updated_at,
                                content=page.content,
                            )
                        )
                    else:
                        continue
                else:
                    ns.create_notion_object(
                        db,
                        NotionCreateSchema(
                            page_id=page.page_id,
                            updated_at=page.updated_at,
                            content=page.content,
                        )
                    )

    return Response(content="Notion data updated", status_code=201)


@router.post(
    "/notion/embedding",
    summary="Update Notion data",
    status_code=status.HTTP_201_CREATED,
    response_class=Response
)
def run_notion_embedding(db: Session = Depends(get_db)) -> Response:
    """
    Endpoint to load and update data from Notion to SQLite
    """
    notion_objects = ns.get_all_notion_objects(db)
    for notion_object in notion_objects:
        if notion_object.embedded_at is None or notion_object.embedded_at < notion_object.updated_at:
            chunks = split_files(data=notion_object.content)
            save_to_pinecone(chunks)
            ns.update_notion_embedding(
                session=db,
                page_id=notion_object.page_id
            )
        else:
            continue

    return Response(content="Notion data updated", status_code=201)
