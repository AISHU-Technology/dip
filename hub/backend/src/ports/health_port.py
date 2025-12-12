"""
Health Check Port Interfaces

Defines the abstract interfaces (ports) for health check operations.
Following the hexagonal architecture pattern, these ports define
the contract between the domain layer and the infrastructure layer.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from src.domains.health import HealthCheckResult, ReadyCheckResult


class HealthCheckPort(ABC):
    """
    Port interface for health check operations.
    
    This is an output port (driven port) that defines
    how the application interacts with external health check mechanisms.
    """
    
    @abstractmethod
    def check_health(self) -> HealthCheckResult:
        """
        Perform a health check.
        
        Returns:
            HealthCheckResult: The result of the health check.
        """
        pass
    
    @abstractmethod
    def check_ready(self) -> ReadyCheckResult:
        """
        Perform a readiness check.
        
        Returns:
            ReadyCheckResult: The result of the readiness check.
        """
        pass
    
    @abstractmethod
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get service information.
        
        Returns:
            Dict[str, Any]: Service information including version, name, etc.
        """
        pass

