import pytest
from httpx import AsyncClient
from app.main import app
from app.core.database import connect_to_mongo, close_mongo_connection
import os
from unittest.mock import patch

@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running!"}

@pytest.mark.asyncio
@patch("app.core.database.AsyncIOMotorClient")
async def test_database_connection(mock_motor):
    # Test successful connection
    os.environ["MONGO_URI"] = "mongodb://localhost:27017"
    await connect_to_mongo()
    mock_motor.assert_called_once()
    
    # Test missing URI connection
    os.environ["MONGO_URI"] = ""
    await connect_to_mongo()  # Should handle gracefully based on our code
    
    # Test shutdown
    await close_mongo_connection()