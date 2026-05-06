import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    logging.info("Connecting to MongoDB Atlas...")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "ai_qa_db")
    
    if not mongo_uri:
        logging.error("MONGO_URI environment variable not set!")
        return

   
    db_instance.client = AsyncIOMotorClient(mongo_uri)
    db_instance.db = db_instance.client[db_name]
    logging.info("Successfully connected to MongoDB!")

async def close_mongo_connection():
    logging.info("Closing MongoDB connection...")
    if db_instance.client:
        db_instance.client.close()
        logging.info("MongoDB connection closed.")

def get_db():
    """Helper function to get the database instance in other files."""
    return db_instance.db