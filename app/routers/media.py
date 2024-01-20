import os
import shutil

from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi import Response
from ai.vector import split_files
from ai.vector import save_to_pinecone
from ai.sql_chat_history import get_all_conversations
from ai.integration.notion import NotionAPI, DatabaseParser


router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post("/upload")
def upload_file(uploaded_file: UploadFile = File(...)):
    path = f"media/{uploaded_file.filename}"

    available_files = [".pdf", ".csv", ".json", ".md", ".txt"]
    if not uploaded_file.filename.endswith(tuple(available_files)):
        return Response(content="Invalid file type", status_code=400)

    with open(path, "w+b") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return {
        "filename": uploaded_file.filename,
        "path": path
    }


@router.get("/file")
def get_file_list():
    root_path = "media"
    # Return files with full path
    pdf_files = [os.path.join(root_path, f) for f in os.listdir(root_path)]

    return pdf_files


# @router.delete("/file/{path}")
# def delete_file(path: str):
#     try:
#         os.remove(path)
#         return {"message": "File deleted successfully"}
#     except FileNotFoundError:
#         return {"message": "File not found"}
#     except Exception as e:
#         return {"error": str(e)}


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

    return {"message": "Embedding completed"}


@router.post("/embedding/chat")
def run_embedding_chat():
    """
    Load all conversations and messages, split into chunks and load to pinecone vector db
    """

    # session_id is not required here
    conversations = get_all_conversations()
    for conversation in conversations:
        chunks = split_files(data=conversation)
        save_to_pinecone(chunks)

    return {"message": "Embedding completed"}


@router.post("/embedding/notion")
def run_embedding_notion():
    """
    Load all databases into vector db
    """

    # session_id is not required here
    # notion = NotionAPI(token=os.getenv("NOTION_API_KEY"), category=Categories.LEARNING)
    # pages = notion.get_database_data(database_id=os.getenv("NOTION_RESOURCES_ID"))
    # parse_pages = DatabaseParser().parse(pages)
    #
    # for page in parse_pages:
    #     content = notion.get_page_content(page_id=page)
    #
    #     page_parser = PageParser()
    #     parsed_content = page_parser.parse(content)
    #     print(parsed_content)