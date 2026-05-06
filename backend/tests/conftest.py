import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db
from unittest.mock import AsyncMock


@pytest.fixture
def mock_db():
    mock = AsyncMock()
   
    mock.documents.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
    
  
    mock.documents.find_one.return_value = {
        "_id": "507f1f77bcf86cd799439011",
        "content": "This is mock document content."
    }
    return mock


@pytest.fixture
def override_get_db(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(override_get_db):
   
    transport = ASGITransport(app=app)
    
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client