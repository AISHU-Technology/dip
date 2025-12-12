"""
Health Check API Schemas

Pydantic models for health check API requests and responses.
"""
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""
    
    status: str = Field(..., description="Health status (healthy, unhealthy, degraded)")
    message: str = Field(..., description="Health status message")
    version: Optional[str] = Field(None, description="Service version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "Service is healthy",
                "version": "1.0.0"
            }
        }


class ReadyResponse(BaseModel):
    """Response schema for ready check endpoint."""
    
    status: str = Field(..., description="Ready status (ready, not_ready)")
    message: str = Field(..., description="Ready status message")
    checks: Optional[Dict[str, Any]] = Field(None, description="Detailed check results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ready",
                "message": "Service is ready to accept requests",
                "checks": {
                    "uptime_seconds": 120.5,
                    "dependencies": "ok"
                }
            }
        }


class ServiceInfoResponse(BaseModel):
    """Response schema for service info endpoint."""
    
    name: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "DIP Hub",
                "version": "1.0.0",
                "uptime_seconds": 120.5
            }
        }

