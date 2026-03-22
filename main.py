"""FastAPI application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import urls, scraping, chat, admin, settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Competitive Intelligence Chatbot API",
    description="AI-powered competitive intelligence system with web scraping, RAG, and vector search",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(urls.router)
app.include_router(scraping.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(settings.router)


@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    init_db()
    logger.info("Database initialized successfully")
    logger.info("Competitive Intelligence Chatbot API is ready!")


@app.get("/")
def root():
    return {
        "name": "Competitive Intelligence Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
