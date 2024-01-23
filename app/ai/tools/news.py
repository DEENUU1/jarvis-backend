from typing import Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from newsapi import NewsApiClient
from config.settings import settings


newsapi = NewsApiClient(api_key=settings.NEWS_API)


def get_top_headlines_formatted() -> str:
    # Get top headlines
    result = ""

    top_headlines = newsapi.get_top_headlines()

    articles = top_headlines["articles"]
    for idx, article in enumerate(articles):
        title = f"{idx} + {article['title']} + '\n' "
        result += title
        result += f"Description: {article["description"]} + '\n'"

    return result


class NewsTool(BaseTool):
    name = "news_tool"
    description = "Useful for when you need to answer questions about current news"

    def _run(
            self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return get_top_headlines_formatted()

    async def _arun(
            self, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
