from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import your database and routes
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import upload

app = FastAPI(
    title="AI-Powered Document & Multimedia Q&A API",
    description="Backend for SDE-1 Assignment",
    version="1.0.0"
)

# Configure CORS for the frontend
origins = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:5173"]').strip("][").replace('"', '').split(", ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include the API Routes (Views)
app.include_router(upload.router, prefix="/api/v1", tags=["Files"])

@app.get("/")
async def root():
    return {"message": "API is running!"}