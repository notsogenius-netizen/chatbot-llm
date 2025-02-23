from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200, length_function=len)
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(persist_directory="./chroma_db", embedding_function= embedding_function)

def load_and_split_document(file_path: str) -> List[Document]:
    if not file_path.endswith(".pdf"):
        raise ValueError("Only PDF files are supported")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        
        for split in splits:
            split.metadata['file_id'] = file_id
        
        vector_store.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int):
    try:
        docs = vector_store.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks.")
        
        vector_store._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents.")
        
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False