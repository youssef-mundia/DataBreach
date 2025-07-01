"""
Application settings and configuration
"""
from typing import Optional, List
from pydantic import BaseSettings, validator
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "DataBreach Monitor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "databreach"
    POSTGRES_PASSWORD: str = "databreach123"
    POSTGRES_DB: str = "databreach"
    POSTGRES_PORT: int = 5432
    
    # Redis
    REDIS_URL: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Tor Configuration
    TOR_PROXY_HOST: str = "127.0.0.1"
    TOR_PROXY_PORT: int = 9050
    TOR_CONTROL_PORT: int = 9051
    TOR_PASSWORD: Optional[str] = None
    
    # Telegram Configuration
    TELEGRAM_API_ID: Optional[int] = None
    TELEGRAM_API_HASH: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_SESSION_STRING: Optional[str] = None
    
    # AI Configuration
    HUGGINGFACE_TOKEN: Optional[str] = None
    LLAMA_MODEL_PATH: Optional[str] = None
    AI_MODEL_NAME: str = "meta-llama/Llama-2-7b-chat-hf"
    
    # CAPTCHA Services
    TWOCAPTCHA_API_KEY: Optional[str] = None
    ANTICAPTCHA_API_KEY: Optional[str] = None
    
    # Scraping Configuration
    USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_DELAY: float = 1.0
    
    # Alert Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SLACK_WEBHOOK_URL: Optional[str] = None
    
    # Monitoring
    PROMETHEUS_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
    
    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"redis://{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/{values.get('REDIS_DB')}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()