from langchain.vectorstores import Chroma

from .embedding import get_embedding_func


def save_to_chroma_db(data):
    vector_db = Chroma.from_documents(
        data,
        get_embedding_func(),
        persist_directory="./chroma_db"
    )
    vector_db.persist()


def get_chroma_db():
    return Chroma(persist_directory="./chroma_db", embedding_function=get_embedding_func())
