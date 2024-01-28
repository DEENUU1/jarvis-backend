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
    description = "Useful when you need to create event in Google Calendar, use current_time_tool to get current date"
    args_schema: Type[BaseModel] = GoogleCalendarCreateEventInput

    def _run(
            self,
            calendar_type: str,
            event_name: str,
            all_day: bool,
            start_date: str,
            end_date: Optional[str] = None,
            duration: Optional[str] = None
    ):
        try:
            return requests.post(
                settings.MAKE_GOOGLE_CALENDAR_CREATE_EVENT,
                data={
                    "calendar_type": calendar_type,
                    "event_name": event_name,
                    "all_day": all_day,
                    "start_date": start_date,
                    "end_date": end_date,
                    "duration": duration,
                }
            )
        except Exception as e:
            print(e)

    def _arun(self, url: str):
        raise NotImplementedError("error here")
