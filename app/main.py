from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
import os
from dotenv import load_dotenv

# from app.routes import auth, submissions, chat, dashboard

load_dotenv()

app = FastAPI(
    title="CodeMentor AI",
    description="AI-powered code explanation platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Routes (commented out until created)
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(submissions.router, prefix="/api/submissions", tags=["submissions"])
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
