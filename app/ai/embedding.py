from langchain.embeddings import OpenAIEmbeddings

from config.settings import settings


def get_embedding_func():
    return OpenAIEmbeddings(model_name="text-embedding-ada-002", openai_api_key=settings.OPENAI_KEY)
