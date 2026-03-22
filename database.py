"""SQLite database models and session management."""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone
from config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), nullable=False, unique=True)
    domain = Column(String(255), nullable=True)
    title = Column(String(512), nullable=True)
    status = Column(String(50), default="pending")  # pending, scraping, scraped, failed
    last_scraped = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    chunks_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    scrape_jobs = relationship("ScrapeJob", back_populates="url_record", cascade="all, delete-orphan")


class ScrapeJob(Base):
    __tablename__ = "scrape_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    status = Column(String(50), default="queued")  # queued, running, completed, failed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    pages_scraped = Column(Integer, default=0)
    chunks_generated = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    url_record = relationship("URL", back_populates="scrape_jobs")


class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)  # JSON string of source URLs
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=True)
    chunk_id = Column(String(100), unique=True, nullable=False)  # ChromaDB doc ID
    source_url = Column(String(2048), nullable=False)
    title = Column(String(512), nullable=True)
    content_preview = Column(Text, nullable=True)  # First 200 chars
    chunk_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
