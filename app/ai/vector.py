import os
from typing import Optional, List

from langchain.document_loaders import PyPDFLoader, CSVLoader, JSONLoader, UnstructuredMarkdownLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain.docstore.document import Document
from config.settings import settings

os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY


def get_embedding_func() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)


def save_to_pinecone(data: List[Document], index_name: str):
    vector_db = Pinecone.from_documents(
        data,
        get_embedding_func(),
        index_name=index_name,
    )
    return vector_db


def get_pinecone(index_name: str) -> Pinecone:
    return Pinecone.from_existing_index(
        index_name=index_name,
        embedding=get_embedding_func(),
    )


class DataLoaderFactory:
    @staticmethod
    def split_docs(file_path: str):
        if file_path.endswith(".pdf"):
            return PyPDFLoader(file_path)
        elif file_path.endswith(".csv"):
            return CSVLoader(file_path)
        elif file_path.endswith(".json"):
            return JSONLoader(file_path)
        elif file_path.endswith(".md"):
            return UnstructuredMarkdownLoader(file_path)
        elif file_path.endswith(".txt"):
            return TextLoader(file_path)
        else:
            raise ValueError("Invalid file type")


def create_document_from_string(data: str) -> Document:
    return Document(page_content=data, metadata={"source": "local"})


def split_files(file_path: Optional[str] = None, data: Optional[str] = None) -> List[Document]:
    """
    Split files into chunks
    """
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    if not file_path:
        split_text = text_splitter.split_text(data)
        documents = []
        for text in split_text:
            documents.append(create_document_from_string(text))
    else:
        loader = DataLoaderFactory().split_docs(file_path=file_path)
        document = loader.load()

        documents = text_splitter.split_documents(document)

    return documents
