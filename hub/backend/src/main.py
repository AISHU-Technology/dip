"""
DIP Hub Application Entry Point

This is the main entry point for the FastAPI application.
It assembles dependencies (injects adapter implementations) and starts the web service.
"""
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Add project root to Python path for module imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.settings import get_settings, Settings
from src.infrastructure.container import init_container, get_container
from src.infrastructure.logging.logger import setup_logging
from src.routers.health_router import create_health_router


def create_app(settings: Settings = None) -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Args:
        settings: Application settings. If None, uses default settings.
    
    Returns:
        FastAPI: The configured application.
    """
    if settings is None:
        settings = get_settings()
    
    # Setup logging
    logger = setup_logging(settings)
    
    # Initialize dependency injection container
    container = init_container(settings)
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan manager."""
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        logger.info(f"Server running on {settings.host}:{settings.port}")
        
        # Mark service as ready after initialization
        container.set_ready(True)
        logger.info("Service is ready to accept requests")
        
        yield
        
        # Cleanup on shutdown
        logger.info("Shutting down service")
        container.set_ready(False)
    
    # Create FastAPI application
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routers
    health_router = create_health_router(container.health_service)
    app.include_router(health_router, prefix=settings.api_prefix)
    
    return app


# Create the application instance
app = create_app()


def main():
    """Run the application using uvicorn."""
    settings = get_settings()
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()

