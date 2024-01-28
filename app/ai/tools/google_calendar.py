from typing import Type, Optional

import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from config.settings import settings


class GoogleCalendarCreateEventInput(BaseModel):
    """Inputs for creating Notion Note page """
    calendar_type: str = Field(
        description=f"Type of calendar in which you can create event, choose based on context or user input. "
                    f"You can use: {settings.GOOGLE_CALENDAR_NAMES}"
    )
    event_name: str = Field(description="Name of the event")
    all_day: bool = Field(description="If event is all day")
    start_date: str = Field(description="Start date of the event in format 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DD'")
    end_date: Optional[str] = Field(description="End date of the event in format 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DD'")
    duration: Optional[str] = Field(
        description="Duration of the event in format HH:mm use only when user gives use duration of an event"
    )


class GoogleCalendarCreateEventTool(BaseTool):
    name = "google_calendar_create_event_tool"
    description = "Useful when you need to create event in Google Calendar "
    args_schema: Type[BaseModel] = GoogleCalendarCreateEventInput

    def _run(self, content: str):
        try:
            return requests.post(
                settings.MAKE_GOOGLE_CALENDAR_CREATE_EVENT,
                data={
                    "calendar_type": self.args_schema.calendar_type,
                    "event_name": self.args_schema.event_name,
                    "all_day": self.args_schema.all_day,
                    "start_date": self.args_schema.start_date,
                    "end_date": self.args_schema.end_date,
                    "duration": self.args_schema.duration,
                }
            )
        except Exception as e:
            print(e)

    def _arun(self, url: str):
        raise NotImplementedError("error here")
