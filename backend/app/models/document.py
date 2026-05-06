from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    summary: str
    timestamps: Optional[List[Dict[str, str]]] = []
    upload_date: datetime

class QuestionRequest(BaseModel):
    document_id: str
    question: str