import os
from typing import Literal, Optional, List, ClassVar
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    DEBUG: Literal["False", "True"] = os.getenv("DEBUG")
    TITLE: str = os.getenv("TITLE")

    # SQLite
    SQLITE_CONNECTION_STRING: Optional[str] = os.getenv("SQLITE_CONNECTION_STRING")

    # AI
    MODELS: ClassVar = os.getenv("MODELS").split(",")


settings = Settings()
