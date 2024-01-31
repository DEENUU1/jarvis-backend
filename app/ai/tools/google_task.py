from typing import Type, Optional, List
import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from config.settings import settings


class GoogleTaskCreateInput(BaseModel):
    event_name: str = Field(description="Short description of an task")


class GoogleTaskListInput(BaseModel):
    start_date: str = Field(description="Start date of the task in format 'YYYY/MM/DD'")

