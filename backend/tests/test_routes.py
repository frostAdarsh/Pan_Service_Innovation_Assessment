import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
import io
from app.main import app
from app.core.database import get_db

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
@patch("app.routes.upload.PyPDF2.PdfReader")
@patch("app.routes.upload.generate_summary_and_timestamps")
async def test_upload_document_pdf(mock_gen_summary, mock_pdf_reader, async_client: AsyncClient):
    
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Extracted PDF text"
    
    mock_reader_instance = MagicMock()
    mock_reader_instance.is_encrypted = False
    mock_reader_instance.pages = [mock_page]
    mock_pdf_reader.return_value = mock_reader_instance

    mock_gen_summary.return_value = {"summary": "A good PDF", "timestamps": []}
    files = {"file": ("test.pdf", io.BytesIO(b"fake pdf content"), "application/pdf")}
    data = {"user_id": "test_user_123"}

    response = await async_client.post("/api/v1/upload/", files=files, data=data)
    assert response.status_code == 200

@pytest.mark.asyncio
@patch("app.routes.upload.PyPDF2.PdfReader")
async def test_upload_pdf_encrypted_or_empty(mock_pdf_reader, async_client: AsyncClient):
    
    mock_reader_instance = MagicMock()
    mock_reader_instance.is_encrypted = True
    mock_pdf_reader.return_value = mock_reader_instance

    files = {"file": ("bad.pdf", io.BytesIO(b"fake"), "application/pdf")}
    data = {"user_id": "test_user_123"}
    res1 = await async_client.post("/api/v1/upload/", files=files, data=data)
    assert res1.status_code == 422

   
    mock_reader_instance.is_encrypted = False
    mock_reader_instance.pages = [] 
    res2 = await async_client.post("/api/v1/upload/", files=files, data=data)
    assert res2.status_code == 400

@pytest.mark.asyncio
async def test_upload_unsupported_file(async_client: AsyncClient):
    files = {"file": ("test.txt", io.BytesIO(b"text"), "text/plain")}
    data = {"user_id": "test_user_123"}
    response = await async_client.post("/api/v1/upload/", files=files, data=data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_upload_db_disconnected(async_client: AsyncClient):
    app.dependency_overrides[get_db] = lambda: None
    files = {"file": ("test.mp3", io.BytesIO(b"fake"), "audio/mpeg")}
    data = {"user_id": "test_user_123"}
    
    response = await async_client.post("/api/v1/upload/", files=files, data=data)
    assert response.status_code == 500
    app.dependency_overrides.clear()

@pytest.mark.asyncio
@patch("app.routes.upload.answer_document_question")
async def test_chat_with_document(mock_answer, async_client: AsyncClient):
    mock_answer.return_value = "This is the answer."
    payload = {"document_id": "507f1f77bcf86cd799439011", "question": "What is this?"}
    response = await async_client.post("/api/v1/chat/", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_chat_document_not_found(async_client: AsyncClient, mock_db):
    mock_db.documents.find_one.return_value = None
    payload = {"document_id": "507f1f77bcf86cd799439011", "question": "What is this?"}
    response = await async_client.post("/api/v1/chat/", json=payload)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_all_documents(async_client: AsyncClient):
    response = await async_client.get("/api/v1/documents/test_user_123")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_document(async_client: AsyncClient):
    response = await async_client.delete("/api/v1/documents/507f1f77bcf86cd799439011")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_document_not_found(async_client: AsyncClient, mock_db):
    mock_db.documents.delete_one.return_value.deleted_count = 0
    response = await async_client.delete("/api/v1/documents/507f1f77bcf86cd799439011")
    assert response.status_code == 404