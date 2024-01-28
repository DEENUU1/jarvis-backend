import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from config.settings import settings


class NotionNoteInput(BaseModel):
    """Inputs for creating Notion Note page """
    content: str = Field(description="Content mentioned by the user that was to be saved to Notion")


class NotionNoteCreateTool(BaseTool):
    name = "notion_note_create_tool"
    description = "Useful when you need to create a new Notion page with the content mentioned by the user. "
    args_schema: Type[BaseModel] = NotionNoteInput

    def _run(self, content: str):
        try:
            return requests.post(settings.MAKE_NOTION_CREATE_NOTE, data={"content": content})
        except Exception as e:
            print(e)

    def _arun(self, url: str):
        raise NotImplementedError("error here")