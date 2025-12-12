"""
Health Check Adapter

Infrastructure adapter that implements the HealthCheckPort interface.
This is the concrete implementation that the application uses for health checks.
"""
import time
from typing import Dict, Any

from src.domains.health import (
    HealthCheckResult,
    HealthStatus,
    ReadyCheckResult,
    ReadyStatus,
)
from src.ports.health_port import HealthCheckPort
from src.infrastructure.config.settings import Settings


class HealthAdapter(HealthCheckPort):
    """
    Health check adapter implementation.
    
    This adapter implements the HealthCheckPort interface and provides
    the concrete implementation for health check operations.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the health adapter.
        
        Args:
            settings: Application settings.
        """
        self._settings = settings
        self._start_time = time.time()
        self._is_ready = False
    
    def set_ready(self, ready: bool = True) -> None:
        """
        Set the ready status.
        
        Args:
            ready: Whether the service is ready.
        """
        self._is_ready = ready
    
    def check_health(self) -> HealthCheckResult:
        """
        Perform a health check.
        
        Returns:
            HealthCheckResult: The result of the health check.
        """
        return HealthCheckResult(
            status=HealthStatus.HEALTHY,
            message="Service is healthy",
            version=self._settings.app_version,
        )
    
    def check_ready(self) -> ReadyCheckResult:
        """
        Perform a readiness check.
        
        Returns:
            ReadyCheckResult: The result of the readiness check.
        """
        uptime = time.time() - self._start_time
        
        if self._is_ready:
            return ReadyCheckResult(
                status=ReadyStatus.READY,
                message="Service is ready to accept requests",
                checks={
                    "uptime_seconds": round(uptime, 2),
                    "dependencies": "ok",
                }
            )
        else:
            return ReadyCheckResult(
                status=ReadyStatus.NOT_READY,
                message="Service is not ready yet",
                checks={
                    "uptime_seconds": round(uptime, 2),
                    "dependencies": "initializing",
                }
            )
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get service information.
        
        Returns:
            Dict[str, Any]: Service information.
        """
        return {
            "name": self._settings.app_name,
            "version": self._settings.app_version,
            "uptime_seconds": round(time.time() - self._start_time, 2),
        }

