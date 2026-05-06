import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db

# --- THE BULLETPROOF FAKE DATABASE ---
class FakeCollection:
    def __init__(self):
        self.find_one_result = {"_id": "507f1f77bcf86cd799439011", "content": "This is mock document content."}
        self.delete_count = 1

    async def insert_one(self, *args, **kwargs):
        class MockResult:
            inserted_id = "507f1f77bcf86cd799439011"
        return MockResult()

    async def find_one(self, *args, **kwargs):
        return self.find_one_result

    async def delete_one(self, *args, **kwargs):
        class MockResult:
            deleted_count = self.delete_count
        return MockResult()

    def find(self, *args, **kwargs):
        class FakeSortedCursor:
            async def to_list(self, length=100):
                return [{"_id": "507f1f77bcf86cd799439011", "filename": "test.pdf"}]
        
        class FakeCursor:
            def sort(self, *args, **kwargs):
                return FakeSortedCursor()
        return FakeCursor()

class FakeDB:
    def __init__(self):
        self.documents = FakeCollection()

# --- FIXTURES ---
@pytest.fixture
def mock_db():
    return FakeDB()

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