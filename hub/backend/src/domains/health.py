"""
Health Domain Models

Defines the domain models for health check and readiness check.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class ReadyStatus(str, Enum):
    """Ready status enumeration."""
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass
class HealthCheckResult:
    """Domain model for health check result."""
    status: HealthStatus
    message: str
    version: Optional[str] = None
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self.status == HealthStatus.HEALTHY


@dataclass
class ReadyCheckResult:
    """Domain model for ready check result."""
    status: ReadyStatus
    message: str
    checks: Optional[dict] = None
    
    def is_ready(self) -> bool:
        """Check if the service is ready."""
        return self.status == ReadyStatus.READY

