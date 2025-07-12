# application configuration settings using pydantic
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "InterviewAI"
    debug: bool = True
    environment: str = "development"
    # usig sql lite for local development
    database_url: str = "sqlite:///./interview_ai.db"
    redis_url: str = "redis://localhost:6379"
    
    # file upload  for video/audio files
    upload_folder: str = "./uploads"
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: list = [".mp4", ".wav", ".mp3", ".jpg", ".png"]
    
    # ai  - all features use local processing (no api keys needed)
    use_local_ai: bool = True
    mock_ai_responses: bool = True
    
    frontend_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    
    # cors configuration for cross-origin requests
    cors_origins: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # logging configuration for application logs
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    # security configuration for rate limiting
    rate_limit: int = 100  # requests per minute
    enable_rate_limiting: bool = True
    # monitoring configuration for metrics collection
    enable_metrics: bool = True
    metrics_path: str = "./metrics"
    class Config:
        env_file = ".env"
        case_sensitive = False
# create global settings instance
settings = Settings()
# ensure required directories exist for file uploads and logs
os.makedirs(settings.upload_folder, exist_ok=True)
os.makedirs("./logs", exist_ok=True)
os.makedirs(settings.metrics_path, exist_ok=True) 