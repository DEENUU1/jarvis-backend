from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter


def split_pdf(file_path: str) -> ...:
    """
    Split PDF into chunks
    """
    loader = PyPDFLoader(file_path)
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(document)
    return documents



