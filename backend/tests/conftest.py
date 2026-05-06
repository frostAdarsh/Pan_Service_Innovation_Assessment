import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_db():
    mock = MagicMock()
    mock_docs = MagicMock()
    
  
    mock_docs.insert_one = AsyncMock()
    mock_docs.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
    

    mock_docs.find_one = AsyncMock()
    mock_docs.find_one.return_value = {
        "_id": "507f1f77bcf86cd799439011",
        "content": "This is mock document content."
    }
    
    
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock()
    mock_cursor.to_list.return_value = [{"_id": "507f1f77bcf86cd799439011", "filename": "test.pdf"}]
    
    mock_sort = MagicMock()
    mock_sort.sort = MagicMock(return_value=mock_cursor)
    mock_docs.find = MagicMock(return_value=mock_sort)
    
    
    mock_docs.delete_one = AsyncMock()
    mock_docs.delete_one.return_value.deleted_count = 1
    
   
    mock.documents = mock_docs
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