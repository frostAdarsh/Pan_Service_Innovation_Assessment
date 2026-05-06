import pytest
from httpx import AsyncClient
from app.main import app
from app.core.database import get_db
from unittest.mock import AsyncMock

# Mock Database fixture
@pytest.fixture
def mock_db():
    mock = AsyncMock()
    # Mock the insert_one response
    mock.documents.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
    
    # Mock the find_one response for the chat endpoint
    mock.documents.find_one.return_value = {
        "_id": "507f1f77bcf86cd799439011",
        "content": "This is mock document content."
    }
    return mock

# Override the FastAPI dependency to use our mock database
@pytest.fixture
def override_get_db(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides.clear()

# Async test client fixture
@pytest.fixture
async def async_client(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client