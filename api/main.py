from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse
from db_utils import get_chat_history
from llm import get_rag_chain
from db_utils import insert_app_logs
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
    
    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain()
    answer = rag_chain.invoke({
        "input": query_input.question,
        "chat_history": chat_history
    })['answer']

    insert_app_logs(session_id, query_input.query, answer)
    logging.info(f"Session ID: {session_id}, Response: {answer}")
    return QueryResponse(response= answer, sesssion_id= session_id)