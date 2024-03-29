import os
from typing import Literal, Optional, ClassVar, Dict, List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    DEBUG: Literal["False", "True"] = os.getenv("DEBUG")
    TITLE: Optional[str] = os.getenv("TITLE")

    # SQLite
    SQLITE_CONNECTION_STRING: Optional[str] = os.getenv("SQLITE_CONNECTION_STRING")
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX: str = "private"

    # AI
    MODELS: ClassVar = os.getenv("MODELS").split(",")
    OPENAI_KEY: Optional[str] = os.getenv("OPENAI_KEY")

    # USER
    FIRST_NAME: Optional[str] = os.getenv("FIRST_NAME")
    LAST_NAME: Optional[str] = os.getenv("LAST_NAME")
    LOCATION: Optional[str] = os.getenv("CITY")

    # INTEGRATION
    NOTION_DEBUG: bool = os.getenv("NOTION_DEBUG") == "True"
    NOTION_API_KEY: Optional[str] = os.getenv("NOTION_API_KEY")
    NOTION_DATABASES: ClassVar = [db.strip() for db in os.getenv("NOTION_DATABASES", "").split(",") if db.strip()]

    OPENWEATHERAPP_API_KEY: Optional[str] = os.getenv("OPENWEATHERAPP_API_KEY")

    NEWS_API: Optional[str] = os.getenv("NEWS_API")

    MAKE_NOTION_CREATE_NOTE: Optional[str] = os.getenv("MAKE_NOTION_CREATE_NOTE")
    MAKE_GOOGLE_CALENDAR_CREATE_LIST_EVENT: Optional[str] = os.getenv("MAKE_GOOGLE_CALENDAR_CREATE_LIST_EVENT")
    GOOGLE_CALENDAR_NAMES: Optional[str] = os.getenv("GOOGLE_CALENDAR_NAMES")


settings = Settings()
