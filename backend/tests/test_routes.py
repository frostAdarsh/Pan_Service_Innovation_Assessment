import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import io

@pytest.mark.asyncio
@patch("app.routes.upload.transcribe_audio_video")
@patch("app.routes.upload.generate_summary_and_timestamps")
async def test_upload_document_media(mock_gen_summary, mock_transcribe, async_client: AsyncClient):
    # Mock AI responses
    mock_transcribe.return_value = "Audio transcript"
    mock_gen_summary.return_value = {"summary": "A good audio", "timestamps": []}
    
    # Create a dummy file
    file_content = b"fake mp3 content"
    files = {"file": ("test.mp3", io.BytesIO(file_content), "audio/mpeg")}

    response = await async_client.post("/api/v1/upload/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.mp3"
    assert data["summary"] == "A good audio"

@pytest.mark.asyncio
async def test_upload_unsupported_file(async_client: AsyncClient):
    files = {"file": ("test.txt", io.BytesIO(b"text"), "text/plain")}
    response = await async_client.post("/api/v1/upload/", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file format"

@pytest.mark.asyncio
@patch("app.routes.upload.answer_document_question")
async def test_chat_with_document(mock_answer, async_client: AsyncClient):
    mock_answer.return_value = "This is the answer."
    
    payload = {
        "document_id": "507f1f77bcf86cd799439011",
        "question": "What is this?"
    }
    
    response = await async_client.post("/api/v1/chat/", json=payload)
    
    assert response.status_code == 200
    assert response.json()["answer"] == "This is the answer."

@pytest.mark.asyncio
@patch("app.routes.upload.get_db")
async def test_chat_document_not_found(mock_get_db, async_client: AsyncClient):
    # Force the DB to return None for this specific test
    mock_db = AsyncMock()
    mock_db.documents.find_one.return_value = None
    mock_get_db.return_value = mock_db

    payload = {
        "document_id": "507f1f77bcf86cd799439011",
        "question": "What is this?"
    }
    
    # We bypass the dependency override just for this test to force a 404
    from app.main import app
    app.dependency_overrides.clear()
    
    response = await async_client.post("/api/v1/chat/", json=payload)
    assert response.status_code == 404