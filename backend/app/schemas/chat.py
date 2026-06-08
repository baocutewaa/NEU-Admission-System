from pydantic import BaseModel
from typing import List, Optional, Any

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    question: str
    sql: Optional[str] = None
    answer: str
    row_count: int
    tables_used: list[str]
    columns: Optional[list[str]] = None
    rows: Optional[list[list[Any]]] = None