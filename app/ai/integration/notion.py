# from config.settings import settings

import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional, List, Dict

import requests
from dotenv import load_dotenv
from pydantic import Json, BaseModel

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

    def __init__(self, token: str, category: Optional[Categories] = None) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.category = category.value

    def get_database_data(self, database_id: str) -> Optional[Data]:
        endpoint = f"databases/{database_id}/query"
        try:
            response = requests.post(self.BASE_URL + endpoint, headers=self.headers)
            json_data = json.dumps(response.json())
            return Data(category=self.category, data=json_data)
        except Exception as e:
            print(e)

    def get_page_content(self, page_id: str) -> Optional[Data]:
        endpoint = f"blocks/{page_id}/children"
        try:
            response = requests.get(self.BASE_URL + endpoint, headers=self.headers)
            json_data = json.dumps(response.json())
            return Data(category=self.category, data=json_data)
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
    def get_rich_text(object_name: str, result: Dict[str, Any]):
        obj = result.get(object_name, None)
        if not obj:
            return None

        return obj.get("rich_text", None)

    def parse_paragraph(self, result: Dict[str, Any]) -> Optional[str]:
        text = ""

        rich_text = self.get_rich_text("paragraph", result)
        if not rich_text:
            return None

        for obj in rich_text:
            text += obj.get("plain_text", " ")

        return text

    def parse_todo(self, result: Dict[str, Any]) -> Optional[str]:
        text = ""

        rich_text = self.get_rich_text("to_do", result)

        if not rich_text:
            return None

        for obj in rich_text:
            text += obj.get("plain_text", " ")

        return text

    def parse_heading(self, result: Dict[str, Any], number: int) -> Optional[str]:
        text = ""

        rich_text = self.get_rich_text(f"heading_{number}", result)

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

            if result_type == "paragraph":
                paragraph = self.parse_paragraph(result)
                if paragraph:
                    text += paragraph
                    text += "\n"

            elif result_type == "to_do":
                todo = self.parse_todo(result)
                if todo:
                    text += todo
                    text += "\n"

            elif result_type in ["heading_1", "heading_2", "heading_3"]:
                number = int(result_type[-1])
                heading = self.parse_heading(result, number)
                if heading:
                    text += heading
                    text += "\n"

        return text



if __name__ == "__main__":
    notion = NotionAPI(token=os.getenv("NOTION_API_KEY"), category=Categories.LEARNING)
    pages = notion.get_database_data(database_id=os.getenv("NOTION_RESOURCES_ID"))
    parse_pages = DatabaseParser().parse(pages)

    # for page in parse_pages:
    #     content = notion.get_page_content(page_id=page)
    #     print(content)

    content = notion.get_page_content(page_id="95b36a75-3a51-4673-bcb2-aac50d54fc6e")
    page_parser = PageParser()
    print(page_parser.parse(content))
