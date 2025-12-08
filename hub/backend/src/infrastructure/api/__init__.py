"""HTTP API 适配器"""
from .routes import router
from .dependencies import get_app_service

__all__ = ["router", "get_app_service"]

