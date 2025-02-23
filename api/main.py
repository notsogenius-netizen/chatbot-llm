from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse
from db_utils import get_chat_history
from llm import get_rag_chain
from db_utils import insert_app_logs, insert_document, delete_document, get_document_list
from chroma_db import index_document_to_chroma, delete_doc_from_chroma
import logging
import uuid
import os
import shutil

logging.basicConfig(filename='app.log', level=logging.INFO)

app = FastAPI()

@app.post("/query", response_model = QueryResponse)
def query(query_input: QueryInput):
    session_id = query_input.session_id
    logging.info(f"Query: {query_input.query}, Session ID: {session_id}")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain()
    answer = rag_chain.invoke({
        "input": query_input.query,
        "chat_history": chat_history
    })['answer']

    insert_app_logs(session_id, query_input.query, answer)
    logging.info(f"Session ID: {session_id}, Response: {answer}")
    return QueryResponse(response= answer, sesssion_id= session_id)

@app.post("/upload")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")
    
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_id = insert_document(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)
        
        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed.", "file_id": file_id}
        else:
            delete_document(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/list-documents")
def get_documents():
    return get_document_list()

@app.delete("/delete-document/{file_id}")
def delete_document_by_id(file_id: str):
    chroma_success = delete_doc_from_chroma(file_id)

    if chroma_success:
        db_success = delete_document(file_id)
        if db_success:
            return {"message": f"Document with ID {file_id} has been successfully deleted."}
        else:
            return {"message": f"Failed to delete document with ID {file_id} from the database."}
    else:
        return {"message": f"Failed to delete document with ID {file_id} from the Chroma database."}