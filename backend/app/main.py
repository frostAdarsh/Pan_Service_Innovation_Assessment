from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager 
from dotenv import load_dotenv
import os


load_dotenv()


from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import upload


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    await connect_to_mongo() 
    
    yield 
    
   
    await close_mongo_connection() 


app = FastAPI(
    title="AI-Powered Document & Multimedia Q&A API",
    description="Backend for SDE-1 Assignment",
    version="1.0.0",
    lifespan=lifespan 
)


origins = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:5173"]').strip("][").replace('"', '').split(", ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(upload.router, prefix="/api/v1", tags=["Files"])

@app.get("/")
async def root():
    return {"message": "API is running!"}