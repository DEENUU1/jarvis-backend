import os
from typing import Literal, Optional, ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    DEBUG: Literal["False", "True"] = os.getenv("DEBUG")
    TITLE: Optional[str] = os.getenv("TITLE")

    # SQLite
    SQLITE_CONNECTION_STRING: Optional[str] = os.getenv("SQLITE_CONNECTION_STRING")
    PINECONE_INDEX: Optional[str] = os.getenv("PINECONE_INDEX")
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")

    # AI
    MODELS: ClassVar = os.getenv("MODELS").split(",")
    OPENAI_KEY: Optional[str] = os.getenv("OPENAI_KEY")

    # USER
    FIRST_NAME: Optional[str] = os.getenv("FIRST_NAME")
    LAST_NAME: Optional[str] = os.getenv("LAST_NAME")
    LOCATION: Optional[str] = os.getenv("CITY")

    # INTEGRATION
    NOTION_API_KEY: Optional[str] = os.getenv("NOTION_API_KEY")

settings = Settings()
