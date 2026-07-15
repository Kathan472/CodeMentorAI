"""
app/main.py
-----------
Application entry point for CodeMentor AI.

Initialises the FastAPI app, registers all API routers, configures CORS middleware,
and serves the frontend static files from the /frontend directory.

Start the server:
    uvicorn app.main:app --reload
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
from app.database import engine
from app import models

# Load environment variables from .env
load_dotenv()

# ---------------------------------------------------------------------------
# Auto-create database tables on startup (idempotent — safe to run every time)
# ---------------------------------------------------------------------------
models.Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CodeMentor AI",
    description="AI-powered code explanation and mentoring platform",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# Allow all origins during development. For production, replace "*" with your
# deployed frontend domain (e.g. "https://codementorai.vercel.app").
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register API Routers
# ---------------------------------------------------------------------------
from app.routes import auth, execute, chat, dashboard, submissions  # noqa: E402

app.include_router(auth.router,        prefix="/api/auth",        tags=["Authentication"])
app.include_router(execute.router,     prefix="/api/code",        tags=["Code Execution"])
app.include_router(chat.router,        prefix="/api/chat",        tags=["AI Chat"])
app.include_router(dashboard.router,   prefix="/api/dashboard",   tags=["Dashboard"])
app.include_router(submissions.router, prefix="/api/submissions",  tags=["Submissions"])


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    """Returns a simple status to verify the server is up and running."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Serve Frontend Static Files
# The entire /frontend directory is mounted at "/" so index.html is served
# automatically. This makes the app a self-contained monorepo.
# ---------------------------------------------------------------------------
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
