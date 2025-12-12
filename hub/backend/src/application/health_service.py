"""
Health Check Application Service

Application layer service that orchestrates health check operations.
This service uses ports (interfaces) and does not depend on any infrastructure details.
"""
from src.domains.health import HealthCheckResult, ReadyCheckResult
from src.ports.health_port import HealthCheckPort


class HealthService:
    """
    Application service for health check operations.
    
    This service is part of the application layer and orchestrates
    the business logic for health check operations through ports.
    """
    
    def __init__(self, health_port: HealthCheckPort):
        """
        Initialize the health service.
        
        Args:
            health_port: The health check port implementation (injected adapter).
        """
        self._health_port = health_port
    
    def get_health(self) -> HealthCheckResult:
        """
        Get the health status of the service.
        
        Returns:
            HealthCheckResult: The health check result.
        """
        return self._health_port.check_health()
    
    def get_ready(self) -> ReadyCheckResult:
        """
        Get the readiness status of the service.
        
        Returns:
            ReadyCheckResult: The readiness check result.
        """
        return self._health_port.check_ready()
    
    def get_service_info(self) -> dict:
        """
        Get service information.
        
        Returns:
            dict: Service information.
        """
        return self._health_port.get_service_info()

