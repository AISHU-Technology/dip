"""
Logging Configuration

Provides a centralized logging configuration for the application.
"""
import logging
import sys
from typing import Optional

from src.infrastructure.config.settings import Settings


def setup_logging(settings: Optional[Settings] = None) -> logging.Logger:
    """
    Setup application logging.
    
    Args:
        settings: Application settings. If None, uses default settings.
    
    Returns:
        logging.Logger: The configured logger.
    """
    if settings is None:
        from src.infrastructure.config.settings import get_settings
        settings = get_settings()
    
    # Get log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Get application logger
    logger = logging.getLogger(settings.app_name)
    logger.setLevel(log_level)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The logger name.
    
    Returns:
        logging.Logger: The logger.
    """
    return logging.getLogger(name)

