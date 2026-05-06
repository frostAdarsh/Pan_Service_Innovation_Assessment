import pytest
from unittest.mock import patch, mock_open, AsyncMock, MagicMock
from app.controllers.ai_controller import transcribe_audio_video, generate_summary_and_timestamps, answer_document_question
import json

@pytest.mark.asyncio
@patch("app.controllers.ai_controller.client")
async def test_transcribe_audio_video(mock_groq_client):
    
    mock_response = MagicMock()
    mock_response.text = "Mocked transcription text"
    
   
    mock_groq_client.audio.transcriptions.create = AsyncMock(return_value=mock_response)

    with patch("builtins.open", mock_open(read_data=b"dummy audio data")):
        result = await transcribe_audio_video("dummy_path.mp3")
        assert result == "Mocked transcription text"

@pytest.mark.asyncio
@patch("app.controllers.ai_controller.client")
async def test_generate_summary_and_timestamps(mock_groq_client):
   
    mock_choice = MagicMock()
    mock_choice.message.content = '{"summary": "Test Summary", "timestamps": [{"time": "10", "topic": "Intro"}]}'
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
   
    mock_groq_client.chat.completions.create = AsyncMock(return_value=mock_response)

    result = await generate_summary_and_timestamps("Some test text")
    assert result["summary"] == "Test Summary"
    assert len(result["timestamps"]) == 1

@pytest.mark.asyncio
@patch("app.controllers.ai_controller.client")
async def test_generate_summary_invalid_json(mock_groq_client):
    
    mock_choice = MagicMock()
    mock_choice.message.content = 'This is not JSON'
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
   
    mock_groq_client.chat.completions.create = AsyncMock(return_value=mock_response)

    result = await generate_summary_and_timestamps("Some test text")
    
   
    assert result["summary"] == "Failed to parse document."

@pytest.mark.asyncio
@patch("app.controllers.ai_controller.client")
async def test_answer_document_question(mock_groq_client):
    mock_choice = MagicMock()
    mock_choice.message.content = "42"
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
   
    mock_groq_client.chat.completions.create = AsyncMock(return_value=mock_response)

    result = await answer_document_question("Context here", "What is the answer?")
    assert result == "42"