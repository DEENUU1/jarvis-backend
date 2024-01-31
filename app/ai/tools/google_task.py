from typing import Type, Any

import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from config.settings import settings


class GoogleTaskCreateInput(BaseModel):
    event_name: str = Field(description="Short description of an task")
    start_date: str = Field(description="Start date of the task in format 'YYYY/MM/DD'")


class GoogleTaskListInput(BaseModel):
    start_date: str = Field(description="Start date of the task in format 'YYYY/MM/DD'")


class GoogleTaskListTool(BaseTool):
    name = "google_task_list_tool"
    description = "Useful when you need to list tasks in Google Calendar"
    args_schema: Type[BaseModel] = GoogleTaskListInput

    def _run(self, start_date: str):
        try:
            response = requests.post(
                settings.MAKE_GOOGLE_CALENDAR_CREATE_LIST_EVENT,
                data={
                    "start_date": start_date,
                    "operation": "task_list"
                }

            )
            return response.text
        except Exception as e:
            print(e)
            raise e

    def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Not implemented")


class GoogleTaskCreateTool(BaseTool):
    name = "google_task_create_tool"
    description = "Useful when you need to create a task in Google Calendar"
    args_schema: Type[BaseModel] = GoogleTaskCreateInput

    def _run(self, event_name: str, start_date: str):
        try:
            return requests.post(
                settings.MAKE_GOOGLE_CALENDAR_CREATE_LIST_EVENT,
                data={
                    "event_name": event_name,
                    "start_date": start_date,
                    "operation": "task_create"
                }
            )
        except Exception as e:
            print(e)
            raise e

    def _arun(self):
        raise NotImplementedError("Not implemented")
