import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional, List, Dict

import requests
from pydantic import Json, BaseModel

from config.settings import settings


class Categories(Enum):
    """
    Name of category based on data collected in notion database
    While using Pinecone the name of the category should have the same name as a index in vector database
    """
    LEARNING = "learning"
    WORK = "work"
    PRIVATE = "private"
    IT = "it"


def get_map_category() -> Dict[Categories, List[str]]:
    map = {
        Categories.LEARNING: [
            settings.NOTION_RESOURCES_ID,
            settings.NOTION_LEARNING_ID,
            settings.NOTION_I_SEMESTR_ID,
        ],
        Categories.WORK: [
            settings.NOTION_USEME_ID,
            settings.NOTION_AS_ID,
            settings.NOTION_UDEMY_ID,
            settings.NOTION_DODATKOWE_ID
        ],
        Categories.PRIVATE: [
            settings.NOTION_NOTES_ID,
            settings.NOTION_BOOKS_ID,
            settings.NOTION_QUOTES_ID
        ],
        Categories.IT: [
            settings.NOTION_PROJECTS_ID,
            settings.NOTION_PROGRAMMING_ID,
            settings.NOTION_DATASTRUCTURES_ID,
            settings.NOTION_ALGORITHMS_ID,
            settings.NOTION_TLACYWN_ID,
            settings.NOTION_COMPUTERS_ID,
        ]
    }

    if settings.NOTION_DEBUG:
        print(map)

    return map


class Data(BaseModel):
    data: Json[Any]
    category: Optional[str] = None


class NotionAPI:
    BASE_URL: str = "https://api.notion.com/v1/"

    def __init__(self, token: str, category: Optional[Categories] = None) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.category = category.value
        self.debug = settings.NOTION_DEBUG

        if self.debug:
            print(f"Run NotionAPI for {self.category}")

    def get_database_data(self, database_id: str) -> Optional[Data]:
        endpoint = f"databases/{database_id}/query"
        try:
            response = requests.post(self.BASE_URL + endpoint, headers=self.headers)
            if self.debug:
                print(response.status_code)

            json_data = json.dumps(response.json())
            if self.debug:
                print(json_data)

            return Data(category=self.category, data=json_data)
        except Exception as e:
            print(e)

    def get_page_content(self, page_id: str) -> Optional[Data]:
        endpoint = f"blocks/{page_id}/children"
        try:
            response = requests.get(self.BASE_URL + endpoint, headers=self.headers)
            if self.debug:
                print(response.status_code)

            json_data = json.dumps(response.json())
            if self.debug:
                print(json_data)

            return Data(category=self.category, data=json_data)
        except Exception as e:
            print(e)


class Parser(ABC):
    def __init__(self):
        self.debug = settings.NOTION_DEBUG

    @abstractmethod
    def parse(self, response) -> None:
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

        if self.debug:
            print(result)

        return result


class PageParser(Parser):
    VALID_OBJECTS = [
        "paragraph",
        "to_do",
        "heading_1",
        "heading_2",
        "heading_3",
        "bulleted_list_item",
        "numbered_list_item",
        "toggle",
        "quote",
        "callout",
    ]

    @staticmethod
    def parse_object(object_name: str, result: Dict[str, Any]) -> Optional[str]:
        text = ""

        obj = result.get(object_name, None)
        if not obj:
            return None

        rich_text = obj.get("rich_text", None)
        if not rich_text:
            return None

        for obj in rich_text:
            text += obj.get("plain_text", " ")

        return text

    def parse(self, data: Data) -> Optional[str]:
        results = data.data.get("results", None)

        if not results:
            return None

        text = ''

        for result in results:
            result_type = result.get("type", None)
            if not result_type or result_type not in self.VALID_OBJECTS:
                continue

            plain_text = self.parse_object(result_type, result)

            if plain_text:
                text += plain_text
                text += "\n"

        if self.debug:
            print(text)

        return text

# if __name__ == "__main__":
#     notion = NotionAPI(token=os.getenv("NOTION_API_KEY"), category=Categories.LEARNING)
#     pages = notion.get_database_data(database_id=os.getenv("NOTION_RESOURCES_ID"))
#     parse_pages = DatabaseParser().parse(pages)
#
#     for page in parse_pages:
#         content = notion.get_page_content(page_id=page)
#
#         page_parser = PageParser()
#         parsed_content = page_parser.parse(content)
#         print(parsed_content)


def notion(category: Categories, dbs: str) -> List[Optional[str]]:
    notion_api = NotionAPI(
        token=settings.NOTION_API_KEY, category=category
    )
    pages = notion_api.get_database_data(database_id=dbs)
    parse_pages = DatabaseParser().parse(pages)

    parsed_pages = []

    for page in parse_pages:
        content = notion_api.get_page_content(page_id=page)
        page_parser = PageParser()
        parsed_content = page_parser.parse(content)
        parsed_pages.append(parsed_content)

    return parsed_pages
