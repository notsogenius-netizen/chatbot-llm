from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse
import logging
import uuid


logging.basicConfig(filename='app.log', level=logging.INFO)

app = FastAPI()

@app.post("/query", response_model = QueryResponse)
def query(query_input: QueryInput):
    session_id = query_input.session_id
    logging.info(f"Query: {query_input.query}, Session ID: {session_id}")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    