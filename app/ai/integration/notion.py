# from config.settings import settings

from enum import Enum
from typing import Any, Optional, List
import requests
from dotenv import load_dotenv
from pydantic import Json, BaseModel
from abc import ABC, abstractmethod

load_dotenv()


class Categories(Enum):
    LEARNING = "learning"
    WORK = "work"
    LIFE = "life"
    IT = "it"


class Data(BaseModel):
    data: Json[Any]
    category: Optional[str] = None


class NotionAPI:
    BASE_URL: str = "https://api.notion.com/v1/"

    def __init__(self, token: str, category: Optional[Categories] = None):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.category = category.value

    def get_database_data(self, database_id: str) -> Data | None:
        endpoint = f"databases/{database_id}/query"
        try:
            response = requests.post(self.BASE_URL + endpoint, headers=self.headers)
            return Data(category=self.category, data=response.json())
        except Exception as e:
            print(e)

    def get_page_content(self, page_id: str):
        endpoint = f"pages/{page_id}"
        try:
            response = requests.get(self.BASE_URL + endpoint, headers=self.headers)
            return Data(category=self.category, data=response.json())
        except Exception as e:
            print(e)


class Parser(ABC):
    @abstractmethod
    def parse(self, response):
        pass


class DatabaseParser(Parser):
    def parse(self, data: Data) -> List[Optional[str]]:
        result = []

        responses = data.data.get("results", None)

        if not responses:
            return []

        for response in responses:
            page_id = response.get("id", None)
            if page_id:
                result.append(page_id)

        return result
