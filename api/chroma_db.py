from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200, length_function=len)
embedding_function = SentenceTransformer("all-MiniLM-L6-v2")
vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

def load_and_split_document(file_path: str) -> List[Document]:
    if not file_path.endswith(".pdf"):
        raise ValueError("Only PDF files are supported")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return text_splitter.split_documents(documents)



