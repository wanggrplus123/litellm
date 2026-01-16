"""
Configuration module for the LangChain chat application.
Manages environment variables and application settings.
"""
import os
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_URL: Optional[str] = os.getenv(
        "REDIS_URL",
        "redis://r-wz9w8s89@r-wz9w8sg55t5vs1hdfxpd.redis.rds.aliyuncs.com:6379/0"
    )
    
    # LLM Configuration
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "sk-fd786efd5e57c21")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen-turbo")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    
    # Memory Configuration
    SUMMARY_KEY_PREFIX: str = "summary:"
    SUMMARY_MIN_LENGTH: int = 500  # Minimum summary length in characters
    
    # API Configuration
    API_TITLE: str = "LangChain Chat API with Memory"
    API_VERSION: str = "1.0.0"


# Global settings instance
settings = Settings()
