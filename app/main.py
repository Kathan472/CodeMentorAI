from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from dotenv import load_dotenv

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

# Import Routes
from app.routes import auth

# Include Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
