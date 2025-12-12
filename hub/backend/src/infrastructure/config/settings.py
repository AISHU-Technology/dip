"""
Application Settings Configuration

Uses pydantic-settings for configuration management.
Settings can be configured via environment variables or .env file.
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    
    All settings can be configured via environment variables.
    Environment variables should be prefixed with 'DIP_HUB_'.
    """
    
    model_config = SettingsConfigDict(
        env_prefix="DIP_HUB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application settings
    app_name: str = Field(default="DIP Hub", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of workers")
    
    # API settings
    api_prefix: str = Field(default="/api/internal/dip-hub/v1", description="API prefix")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Logging format"
    )
    
    # Health check settings
    health_check_timeout: int = Field(default=5, description="Health check timeout in seconds")


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: The application settings.
    """
    return Settings()

