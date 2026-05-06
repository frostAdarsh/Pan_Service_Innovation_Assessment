from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.controllers.ai_controller import transcribe_audio_video, generate_summary_and_timestamps, answer_document_question
from app.core.database import get_db
from app.models.document import QuestionRequest
import shutil
from datetime import datetime
from bson import ObjectId
import PyPDF2
import tempfile
import os

router = APIRouter()

def extract_pdf_text(file_path: str) -> str:
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if reader.is_encrypted:
                raise ValueError("Cannot read password-protected PDFs.")
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse PDF file: {str(e)}")
    return text.strip()

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...), user_id: str = Form(...)):
    db = get_db()
    if db is None: 
        raise HTTPException(status_code=500, detail="Database not connected")

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        file_location = temp_file.name
    
    try:
        if file.filename.lower().endswith(('.mp3', '.mp4', '.wav', '.mpeg')):
            file_type = "media"
            content = await transcribe_audio_video(file_location)
        elif file.filename.lower().endswith('.pdf'):
            file_type = "pdf"
            content = extract_pdf_text(file_location)
            if not content:
                raise HTTPException(status_code=400, detail="Could not extract text.")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        analysis = await generate_summary_and_timestamps(content, file_type)
        
        doc = {
            "user_id": user_id,
            "filename": file.filename, 
            "file_type": file_type, 
            "content": content,
            "summary": analysis.get("summary", "Summary generation failed."), 
            "timestamps": analysis.get("timestamps", []),
            "keywords": analysis.get("keywords", []), 
            "upload_date": datetime.utcnow()
        }
        res = await db.documents.insert_one(doc)
        
        return {
            "id": str(res.inserted_id), 
            "filename": file.filename, 
            "summary": doc["summary"], 
            "timestamps": doc["timestamps"], 
            "keywords": doc["keywords"], 
            "file_type": file_type
        }
    finally:
        if os.path.exists(file_location): 
            os.remove(file_location)

@router.post("/chat/")
async def chat_with_document(req: QuestionRequest):
    db = get_db()
    doc = await db.documents.find_one({"_id": ObjectId(req.document_id)})
    if not doc: 
        raise HTTPException(status_code=404, detail="Document not found")
    answer = await answer_document_question(doc["content"], req.question)
    return {"answer": answer}

@router.get("/documents/{user_id}")
async def get_all_documents(user_id: str):
    db = get_db()
    cursor = db.documents.find({"user_id": user_id}, {"content": 0}).sort("upload_date", -1)
    documents = await cursor.to_list(length=100)
    for doc in documents:
        doc["id"] = str(doc.pop("_id"))
    return documents

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    db = get_db()
    result = await db.documents.delete_one({"_id": ObjectId(doc_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Deleted successfully"}