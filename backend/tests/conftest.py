import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import patch

# --- THE ASYNC FAKE DATABASE ---
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
    fake_db = FakeDB()
    # THIS FORCE-PATCHES THE DB INSIDE UPLOAD.PY
    with patch("app.routes.upload.get_db", return_value=fake_db):
        yield fake_db

@pytest.fixture
async def async_client(mock_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client