# 🚀 AI-Powered Document & Multimedia Q&A Platform

An intelligent full-stack web application that enables users to upload **PDFs, audio, and video files**, generate **AI-powered summaries**, extract **keywords & timestamps**, and interact with uploaded content through an AI chatbot.

---

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Coverage](https://img.shields.io/badge/Coverage-96.15%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# ✨ Features

✅ Upload PDF, MP3, MP4, WAV, and MPEG files  
✅ AI-generated summaries using Groq AI  
✅ Audio & video transcription support  
✅ Keyword extraction from uploaded documents  
✅ Timestamp/topic extraction for media files  
✅ AI chatbot for uploaded content  
✅ Clerk authentication integration  
✅ MongoDB database integration  
✅ Dockerized full-stack setup  
✅ Automated backend testing with 96.15% coverage  
✅ GitHub Actions CI/CD pipeline  

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
- GitHub Actions

---

# 📁 Project Structure

```bash
Pan_Service_Innovation_Assessment/
│
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       └── test.yml
│
├── docker-compose.yml
├── .env.example
└── README.md
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

# =========================
# Backend CORS
# =========================
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

---

# ⚡ Installation & Setup

# 1️⃣ Clone Repository

```bash
git clone https://github.com/frostAdarsh/Pan_Service_Innovation_Assessment.git
cd Pan_Service_Innovation_Assessment
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

# 🧪 Automated Testing & Coverage

This project includes automated backend testing using `pytest` and `pytest-cov`.

---

# 📦 Install Testing Dependencies

```bash
pip install pytest pytest-cov
```

---

# ▶ Run All Tests

```bash
pytest
```

---

# 📊 Generate Coverage Report

```bash
pytest --cov=app --cov-report=term-missing
```

---

# 🌐 Generate HTML Coverage Report

```bash
pytest --cov=app --cov-report=html
```

Coverage report will be generated inside:

```bash
htmlcov/index.html
```

---

# ✅ Actual Coverage Output

```bash
platform linux -- Python 3.10.20, pytest-9.0.3, pluggy-1.6.0
rootdir: /home/runner/work/Pan_Service_Innovation_Assessment/Pan_Service_Innovation_Assessment/backend
configfile: pytest.ini

collected 17 items

tests/test_controllers.py ....                                           [ 23%]
tests/test_main.py ..                                                    [ 35%]
tests/test_routes.py ...........                                         [100%]

================================ tests coverage ================================

Name                               Stmts   Miss  Cover
----------------------------------------------------------------
app/controllers/ai_controller.py      22      1    95%
app/core/database.py                  24      1    96%
app/main.py                           20      3    85%
app/models/document.py                13      0   100%
app/routes/upload.py                  77      1    99%

----------------------------------------------------------------
TOTAL                                156      6    96%

Required test coverage of 95% reached.
Total coverage: 96.15%
```

---

# 🎯 Coverage Summary

| Module | Coverage |
|--------|----------|
| AI Controller | 95% |
| Database Layer | 96% |
| Main Application | 85% |
| Models | 100% |
| Upload Routes | 99% |

---

# ✅ Total Coverage: **96.15%**

---

# 🧪 Tested Features

- File upload APIs
- PDF parsing
- Audio/video transcription
- AI chatbot endpoints
- MongoDB operations
- Authentication flows
- Error handling scenarios
- Invalid request validation
- Timestamp extraction logic
- Summary generation
- Edge case testing

---

# 📸 Test Coverage Proof

![Coverage Screenshot](./screenshots/coverage.png)

---

# ⚙ GitHub Actions CI/CD Pipeline

This project uses GitHub Actions for automated testing.

Location:

```bash
.github/workflows/test.yml
```

---

# 🚀 GitHub Actions Workflow

```yaml
name: Backend Tests

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set Up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install Dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run Tests with Coverage
        run: |
          cd backend
          pytest --cov=app --cov-report=term-missing
```

---

# 🌐 Live Demo

Frontend: https://your-frontend-url.com

Backend Docs: https://your-backend-url.com/docs

---

# 🎥 Walkthrough Video

YouTube / Google Drive Link:

https://your-video-link.com

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

✅ Store secrets in `.env`  
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
