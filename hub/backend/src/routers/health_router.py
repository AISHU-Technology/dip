"""
Health Check Router

FastAPI router for health check endpoints.
This is the interface adapter that handles HTTP requests and delegates to the application layer.
"""
from fastapi import APIRouter, Depends, Response, status

from src.application.health_service import HealthService
from src.routers.schemas.health import HealthResponse, ReadyResponse, ServiceInfoResponse


def create_health_router(health_service: HealthService) -> APIRouter:
    """
    Create the health check router.
    
    Args:
        health_service: The health service instance.
    
    Returns:
        APIRouter: The configured router.
    """
    router = APIRouter(tags=["Health"])
    
    @router.get(
        "/health",
        response_model=HealthResponse,
        summary="Health Check",
        description="Check if the service is healthy.",
        responses={
            200: {"description": "Service is healthy"},
            503: {"description": "Service is unhealthy"},
        }
    )
    async def health_check(response: Response) -> HealthResponse:
        """
        Health check endpoint.
        
        Returns the health status of the service.
        """
        result = health_service.get_health()
        
        if not result.is_healthy():
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        return HealthResponse(
            status=result.status.value,
            message=result.message,
            version=result.version,
        )
    
    @router.get(
        "/ready",
        response_model=ReadyResponse,
        summary="Readiness Check",
        description="Check if the service is ready to accept requests.",
        responses={
            200: {"description": "Service is ready"},
            503: {"description": "Service is not ready"},
        }
    )
    async def ready_check(response: Response) -> ReadyResponse:
        """
        Readiness check endpoint.
        
        Returns the readiness status of the service.
        This indicates whether the service has completed initialization
        and is ready to accept traffic.
        """
        result = health_service.get_ready()
        
        if not result.is_ready():
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        return ReadyResponse(
            status=result.status.value,
            message=result.message,
            checks=result.checks,
        )
    
    @router.get(
        "/info",
        response_model=ServiceInfoResponse,
        summary="Service Info",
        description="Get service information.",
    )
    async def service_info() -> ServiceInfoResponse:
        """
        Service info endpoint.
        
        Returns information about the service.
        """
        info = health_service.get_service_info()
        return ServiceInfoResponse(**info)
    
    return router

