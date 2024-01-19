import os

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Pinecone

from config.settings import settings

os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY


def get_embedding_func():
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)


def save_to_pinecone(data):
    vector_db = Pinecone.from_documents(
        data,
        get_embedding_func(),
        index_name=settings.PINECONE_INDEX,
    )
    return vector_db


def get_pinecone():
    return Pinecone.from_existing_index(
        index_name=settings.PINECONE_INDEX,
        embedding=get_embedding_func(),
    )


def split_files(file_path: str) -> ...:
    """
    Split PDF into chunks
    """
    loader = PyPDFLoader(file_path)
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(document)
    return documents
