from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

# import application configuration and components
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router

# configure logging for the application
def setup_logging():
    # create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # configure logging format with timestamp, module, level, and message
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # configure file handler for  logging
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(file_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()
# this below converts a generator function into aysnc context manager 
# sets up tables, ai models, logging metrics, and handles app termination
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup phase - initialize application components
    logger.info(" Starting Backend...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # create database tables (async version)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(" Database tables created successfully")
    except Exception as e:
        logger.error(f" Failed to create database tables: {e}")
        raise
    
    # log startup metrics and completion
    startup_time = datetime.now()
    logger.info(f" Application startup completed at {startup_time}")
    
    yield
    
    # shutdown phase - cleanup resources
    logger.info(" Shutting down Backend...")

# create fastapi application instance with metadata and lifespan
app = FastAPI(
    title="Interview API",
    description="AI-powered interview coaching platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# cors middleware configuration for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    logger.info(" Root endpoint accessed")
    return {
        "message": "Welcome to InterviewAI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    logger.info(" Health check endpoint accessed")
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f" HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000,  # listen to for incoming connections on this port 
        reload=True,  
        log_level="info"  
    ) 