import pytest
from httpx import AsyncClient
from unittest.mock import patch
import io

@pytest.mark.asyncio
@patch("app.routes.upload.transcribe_audio_video")
@patch("app.routes.upload.generate_summary_and_timestamps")
async def test_upload_document_media(mock_gen_summary, mock_transcribe, async_client: AsyncClient):
   
    mock_transcribe.return_value = "Audio transcript"
    mock_gen_summary.return_value = {"summary": "A good audio", "timestamps": []}

    
    file_content = b"fake mp3 content"
    files = {"file": ("test.mp3", io.BytesIO(file_content), "audio/mpeg")}
    
   
    data = {"user_id": "test_user_123"}

    response = await async_client.post("/api/v1/upload/", files=files, data=data)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_unsupported_file(async_client: AsyncClient):
    files = {"file": ("test.txt", io.BytesIO(b"text"), "text/plain")}
    
  
    data = {"user_id": "test_user_123"}
    
    response = await async_client.post("/api/v1/upload/", files=files, data=data)
    
    assert response.status_code == 400


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


@pytest.mark.asyncio
async def test_get_all_documents(async_client: AsyncClient):
    response = await async_client.get("/api/v1/documents/test_user_123")
    assert response.status_code == 200