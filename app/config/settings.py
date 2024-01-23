import os
from typing import Literal, Optional, ClassVar, Dict

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
    PINECONE_LEARNING_INDEX: str = "learning"
    PINECONE_WORK_INDEX: str = "work"
    PINECONE_PRIVATE_INDEX: str = "private"
    PINECONE_IT_INDEX: str = "it"

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
    NOTION_NOTES_ID: Optional[str] = os.getenv("NOTION_NOTES_ID")
    NOTION_RESOURCES_ID: Optional[str] = os.getenv("NOTION_RESOURCES_ID")
    NOTION_LEARNING_ID: Optional[str] = os.getenv("NOTION_LEARNING_ID")
    NOTION_PROJECTS_ID: Optional[str] = os.getenv("NOTION_PROJECTS_ID")
    NOTION_PROGRAMMING_ID: Optional[str] = os.getenv("NOTION_PROGRAMMING_ID")
    NOTION_DATASTRUCTURES_ID: Optional[str] = os.getenv("NOTION_DATASTRUCTURES_ID")
    NOTION_ALGORITHMS_ID: Optional[str] = os.getenv("NOTION_ALGORITHMS_ID")
    NOTION_TLACYWN_ID: Optional[str] = os.getenv("NOTION_TLACYWN_ID")
    NOTION_COMPUTERS_ID: Optional[str] = os.getenv("NOTION_COMPUTERS_ID")
    NOTION_I_SEMESTR_ID: Optional[str] = os.getenv("NOTION_I_SEMESTR_ID")
    NOTION_BOOKS_ID: Optional[str] = os.getenv("NOTION_BOOKS_ID")
    NOTION_QUOTES_ID: Optional[str] = os.getenv("NOTION_QUOTES_ID")
    NOTION_USEME_ID: Optional[str] = os.getenv("NOTION_USEME_ID")
    NOTION_AS_ID: Optional[str] = os.getenv("NOTION_AS_ID")
    NOTION_UDEMY_ID: Optional[str] = os.getenv("NOTION_UDEMY_ID")
    NOTION_DODATKOWE_ID: Optional[str] = os.getenv("NOTION_DODATKOWE_ID")

    OPENWEATHERAPP_API_KEY: Optional[str] = os.getenv("OPENWEATHERAPP_API_KEY")

    NEWS_API: Optional[str] = os.getenv("NEWS_API")

    GOOGLE_CALENDAR_OSOBISTE: Optional[str] = os.getenv("GOOGLE_CALENDAR_OSOBISTE")
    GOOGLE_CALENDAR_PRACA: Optional[str] = os.getenv("GOOGLE_CALENDAR_PRACA")
    GOOGLE_CALENDAR_STUDIA: Optional[str] = os.getenv("GOOGLE_CALENDAR_STUDIA")
    GOOGLE_CALENDAR_SUBSKRYPCJE_I_OPLATY: Optional[str] = os.getenv("GOOGLE_CALENDAR_SUBSKRYPCJE_I_OPLATY")
    GOOGLE_CALENDAR_URODZINY_ROCZNICE: Optional[str] = os.getenv("GOOGLE_CALENDAR_URODZINY_ROCZNICE")
    GOOGLE_CALENDAR_SWIETA_W_POLSCE: Optional[str] = os.getenv("GOOGLE_CALENDAR_SWIETA_W_POLSCE")

    GOOGLE_CALENDARS: Dict[str, str] = {
            "Private": GOOGLE_CALENDAR_OSOBISTE,
            "Work": GOOGLE_CALENDAR_PRACA,
            "School": GOOGLE_CALENDAR_STUDIA,
            "Payments": GOOGLE_CALENDAR_SUBSKRYPCJE_I_OPLATY,
            "Celebrations": GOOGLE_CALENDAR_URODZINY_ROCZNICE,
            "Polish_holidays": GOOGLE_CALENDAR_SWIETA_W_POLSCE
        }

    GOOGLE_CALENDAR_EMAIL: Optional[str] = os.getenv("GOOGLE_CALENDAR_EMAIL")

    GOOGLE_CALENDAR_DEBUG: bool = os.getenv("GOOGLE_CALENDAR_DEBUG") == "True"


settings = Settings()
