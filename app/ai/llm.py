from langchain_community.chat_models import ChatOpenAI

from config.settings import settings


def get_chat_openai(model: str) -> ChatOpenAI:
    return ChatOpenAI(
        temperature=0,
        model=model,
        openai_api_key=settings.OPENAI_KEY
    )
