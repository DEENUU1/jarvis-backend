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
    LEARNING = settings.PINECONE_LEARNING_INDEX
    WORK = settings.PINECONE_WORK_INDEX
    PRIVATE = settings.PINECONE_PRIVATE_INDEX
    IT = settings.PINECONE_IT_INDEX


def get_map_category() -> Dict[Categories, List[str]]:
    """
    Retrieve a mapping of Categories to corresponding Notion IDs for organization.
    """
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
    """
    A Python client for interacting with the Notion API.
    This class provides methods to retrieve data from Notion databases and pages.
    """
    BASE_URL: str = "https://api.notion.com/v1/"

    def __init__(self, token: str, category: Optional[Categories] = None) -> None:
        """
        Initializes a NotionAPI instance.
        """
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
        """
        Retrieves data from a Notion database.
        """
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
        """
        Retrieves content from a Notion page.
        """
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
    """
    Abstract base class for parsing Notion API responses.

    Attributes:
        debug (bool): Flag indicating whether to print debug information.

    Methods:
        __init__(self): Initializes a Parser instance.
        parse(self, response) -> None: Abstract method to be implemented by subclasses for parsing responses.
    """
    def __init__(self):
        """
        Initializes a Parser instance.
        """
        self.debug = settings.NOTION_DEBUG

    @abstractmethod
    def parse(self, response) -> None:
        """
        Abstract method to be implemented by subclasses for parsing responses.
        """
        pass


class DatabaseParser(Parser):
    """
    Concrete class for parsing Notion database responses.
    """
    def parse(self, data: Data) -> List[Optional[str]]:
        """
        Parses Notion database data.
        """
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
    """
    Concrete class for parsing Notion page responses.
    """
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
        """
        Parses a specific Notion object.
        """
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
        """
        Parses Notion page data and returns the concatenated text.
        """
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


def notion(category: Categories, dbs: str) -> List[Optional[str]]:
    """
    Retrieves and parses Notion data for a given category and database.

    Parameters:
        category (Categories): The category of Notion data to interact with.
        dbs (str): The unique identifier of the Notion database.

    Returns:
        List[Optional[str]]: A list of parsed content from Notion pages.
    """
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