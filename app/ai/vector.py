import os

from langchain.document_loaders import PyPDFLoader, CSVLoader, JSONLoader, UnstructuredMarkdownLoader
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


class DataLoaderFactory:
    def split_docs(self, file_path: str):
        if file_path.endswith(".pdf"):
            return PyPDFLoader(file_path)
        elif file_path.endswith(".csv"):
            return CSVLoader(file_path)
        elif file_path.endswith(".json"):
            return JSONLoader(file_path)
        elif file_path.endswith(".md"):
            return UnstructuredMarkdownLoader(file_path)
        else:
            raise ValueError("Invalid file type")


def split_files(file_path: str) -> ...:
    """
    Split files into chunks
    """
    loader = DataLoaderFactory().split_docs(file_path=file_path)
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(document)
    return documents

