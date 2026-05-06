# 🚀 AI-Powered Document & Multimedia Q&A Platform

An intelligent full-stack application that allows users to upload **PDFs, audio, and video files**, generate **AI-powered summaries**, extract **keywords & timestamps**, and interact with uploaded content using a conversational AI interface.

---

# ✨ Features

✅ Upload and process multiple file formats  
✅ AI-generated summaries using Groq AI  
✅ Audio & video transcription support  
✅ Keyword extraction from documents  
✅ Timestamp/topic generation for media files  
✅ Chat with uploaded documents  
✅ User authentication with Clerk  
✅ Responsive React frontend  
✅ FastAPI backend APIs  
✅ MongoDB database integration  
✅ Dockerized deployment support  

---

# 🛠 Tech Stack

## 🎨 Frontend
- React
- Vite
- TailwindCSS
- React Router
- Clerk Authentication
- Axios

---

## ⚙ Backend
- FastAPI
- MongoDB (Motor Async Driver)
- Groq API
- PyPDF2

---

## 🐳 DevOps
- Docker
- Docker Compose

---

# 📁 Project Structure

```bash
panServiceInnovation/
│
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── .env
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory.

```env
# =========================
# MongoDB Configuration
# =========================
MONGO_URI=your_mongodb_connection_string
DB_NAME=ai_qa_db

# =========================
# Groq API Configuration
# =========================
GROQ_API_KEY=your_groq_api_key

# =========================
# Frontend Configuration
# =========================
VITE_API_URL=http://localhost:8000

# Clerk Authentication
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key


```

---

# ⚡ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd panServiceInnovation
```

---

# ⚙ Backend Setup

## 📂 Navigate to Backend

```bash
cd backend
```

---

## 🐍 Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Run Backend Server

```bash
uvicorn app.main:app --reload
```

### Backend URL

```bash
http://localhost:8000
```

---

# 🎨 Frontend Setup

## 📂 Navigate to Frontend

```bash
cd frontend
```

---

## 📦 Install Frontend Dependencies

```bash
npm install
```

---

## ▶ Run Frontend Development Server

```bash
npm run dev
```

### Frontend URL

```bash
http://localhost:5173
```

---

# 🐳 Docker Setup

## 🚀 Run Full Application

From the project root directory:

```bash
docker-compose up --build
```

---

# 🧩 Docker Services

| Service | Port |
|---------|------|
| Frontend | 5173 |
| Backend | 8000 |

---

# ▶ Running Instructions

## 🔹 Run Backend

```bash
cd backend
uvicorn app.main:app --reload
```

---

## 🔹 Run Frontend

```bash
cd frontend
npm run dev
```

---

# 🏗 Production Build

## 🎨 Frontend Production Build

```bash
npm run build
npm run preview
```

---

## ⚙ Backend Production Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# 📚 API Documentation

## 🌐 Base URL

```bash
http://localhost:8000/api/v1
```

---

# 🔌 API Endpoints

# 1️⃣ Upload Document

## Endpoint

```http
POST /upload/
```

---

## Form Data

| Field | Type | Required |
|------|------|------|
| file | File | ✅ Yes |
| user_id | String | ✅ Yes |

---

## 📂 Supported File Types

- PDF
- MP3
- MP4
- WAV
- MPEG

---

## ✅ Example Response

```json
{
  "id": "6890d7f5e2",
  "filename": "lecture.mp4",
  "summary": "AI generated summary...",
  "timestamps": [
    {
      "time": 30,
      "topic": "Introduction"
    }
  ],
  "keywords": ["AI", "Machine Learning"],
  "file_type": "media"
}
```

---

# 2️⃣ Chat With Document

## Endpoint

```http
POST /chat/
```

---

## Request Body

```json
{
  "document_id": "6890d7f5e2",
  "question": "What is this document about?"
}
```

---

## ✅ Example Response

```json
{
  "answer": "This document discusses..."
}
```

---

# 3️⃣ Get User Documents

## Endpoint

```http
GET /documents/{user_id}
```

---

## ✅ Example Response

```json
[
  {
    "id": "6890d7f5e2",
    "filename": "notes.pdf",
    "summary": "Summary here...",
    "file_type": "pdf"
  }
]
```

---

# 4️⃣ Delete Document

## Endpoint

```http
DELETE /documents/{doc_id}
```

---

## ✅ Example Response

```json
{
  "message": "Deleted successfully"
}
```

---

# 📖 Swagger API Docs

FastAPI automatically generates interactive API documentation.

## Swagger UI

```bash
http://localhost:8000/docs
```

---

## ReDoc Documentation

```bash
http://localhost:8000/redoc
```

---

# 🧪 Testing

## ✅ Run Backend Tests

```bash
pytest
```

---

## ✅ Run Tests with Coverage

```bash
pytest --cov=app
```

---

# 🧹 Linting

## Frontend Linting

```bash
npm run lint
```

---

# ❌ Error Handling

The backend handles:

- Unsupported file formats
- Empty PDFs
- Password-protected PDFs
- Invalid document IDs
- Missing audio tracks
- Database connection failures

---

# 🔒 Security Best Practices

✅ Store secrets in `.env` files  
✅ Never commit API keys  
✅ Configure CORS properly  
✅ Use HTTPS in production  
✅ Restrict upload sizes  
✅ Validate uploaded files  

---

# 🚀 Future Improvements

- JWT Authentication
- Vector Database Search
- Semantic Search
- Multi-language Support
- Streaming AI Responses
- AWS S3 File Storage
- Redis Caching

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

Developed using:

- ⚡ FastAPI
- 🎨 React + Vite
- 🗄 MongoDB
- 🤖 Groq AI
- 🔐 Clerk Authentication

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
