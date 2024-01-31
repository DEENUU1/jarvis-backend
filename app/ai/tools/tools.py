from typing import List

from langchain.chains import RetrievalQA
from langchain.tools import WikipediaQueryRun
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langchain_core.tools import Tool

from . import google_calendar, news, notion, today, google_task
from ai.vector import get_pinecone
from config.settings import settings


def get_tools(llm: ChatOpenAI) -> List[Tool]:
    duckduck_search = DuckDuckGoSearchAPIWrapper()

    personal_data = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_pinecone().as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        ),
    )

    weather = OpenWeatherMapAPIWrapper(openweathermap_api_key=settings.OPENWEATHERAPP_API_KEY)
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    return [
        google_task.GoogleTaskListTool(),
        google_task.GoogleTaskCreateTool(),
        google_calendar.GoogleCalendarCreateEventTool(),
        google_calendar.GoogleCalendarListEventTool(),
        notion.NotionNoteCreateTool(),
        today.CurrentTimeTool(),
        news.NewsTool(),
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="Useful when you need to search information in online encyclopedia. You should ask targeted questions"
        ),
        Tool(
            name="Weather",
            func=weather.run,
            description="Useful for when you need to answer questions about current weather"
        ),
        Tool(
            name="Search",
            func=duckduck_search.run,
            description="Useful for when you need to answer questions about current events. You should ask targeted questions"
        ),
        Tool(
            name="User-private-data",
            func=personal_data.run,
            description="Useful when you need to answer questions about user's personal data, notes, friends, work, learning"
        ),
    ]
