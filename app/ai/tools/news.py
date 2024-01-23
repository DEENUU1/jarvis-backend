from typing import Union, Dict, Tuple
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

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}

    def _run(self) -> str:
        return get_top_headlines_formatted()

    async def _arun(self) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
