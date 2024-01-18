from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


def save_to_chroma_db(data):
    vector_db = Chroma.from_documents(
        documents=data,
        embedding=OpenAIEmbeddings(),
        persist_directory="./data"
    )
    vector_db.persist()
