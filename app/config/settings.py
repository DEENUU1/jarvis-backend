import os
from typing import Literal, Optional, ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    DEBUG: Literal["False", "True"] = os.getenv("DEBUG")
    TITLE: str = os.getenv("TITLE")

    # SQLite
    SQLITE_CONNECTION_STRING: Optional[str] = os.getenv("SQLITE_CONNECTION_STRING")
    PINECONE_INDEX: Optional[str] = os.getenv("PINECONE_INDEX")
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")

    # AI
    MODELS: ClassVar = os.getenv("MODELS").split(",")
    OPENAI_KEY: str = os.getenv("OPENAI_KEY")

    # USER
    FIRST_NAME: str = os.getenv("FIRST_NAME")
    LAST_NAME: str = os.getenv("LAST_NAME")
    LOCATION: str = os.getenv("CITY")


settings = Settings()
