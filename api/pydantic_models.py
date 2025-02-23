from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class QueryInput(BaseModel):
    query: str
    session_id: str = Field(default = None)

class QueryResponse(BaseModel):
    response: str
    sesssion_id: str
