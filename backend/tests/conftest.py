import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_db():
    mock = AsyncMock()
    
   
    insert_result = MagicMock()
    insert_result.inserted_id = "507f1f77bcf86cd799439011"
    mock.documents.insert_one = AsyncMock(return_value=insert_result)
    
   
    mock.documents.find_one = AsyncMock(return_value={
        "_id": "507f1f77bcf86cd799439011",
        "content": "This is mock document content."
    })
    
    
    cursor_mock = AsyncMock()
    cursor_mock.to_list = AsyncMock(return_value=[{"_id": "507f1f77bcf86cd799439011", "filename": "test.pdf"}])
    sort_mock = MagicMock()
    sort_mock.sort.return_value = cursor_mock
    mock.documents.find.return_value = sort_mock
    
   
    delete_result = MagicMock()
    delete_result.deleted_count = 1
    mock.documents.delete_one = AsyncMock(return_value=delete_result)
    
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