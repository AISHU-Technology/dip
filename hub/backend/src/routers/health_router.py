"""
健康检查路由

健康检查端点的 FastAPI 路由。
这是处理 HTTP 请求并委托给应用层的接口适配器。
"""
from fastapi import APIRouter, Depends, Response, status

from src.application.health_service import HealthService
from src.routers.schemas.health import HealthResponse, ReadyResponse, ServiceInfoResponse


def create_health_router(health_service: HealthService) -> APIRouter:
    """
    创建健康检查路由。
    
    参数:
        health_service: 健康服务实例。
    
    返回:
        APIRouter: 配置完成的路由。
    """
    router = APIRouter(tags=["健康检查"])
    
    @router.get(
        "/health",
        response_model=HealthResponse,
        summary="健康检查",
        description="检查服务是否健康。",
        responses={
            200: {"description": "服务健康"},
            503: {"description": "服务不健康"},
        }
    )
    async def health_check(response: Response) -> HealthResponse:
        """
        健康检查端点。
        
        返回服务的健康状态。
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
        summary="就绪检查",
        description="检查服务是否准备好接受请求。",
        responses={
            200: {"description": "服务已就绪"},
            503: {"description": "服务未就绪"},
        }
    )
    async def ready_check(response: Response) -> ReadyResponse:
        """
        就绪检查端点。
        
        返回服务的就绪状态。
        表示服务是否已完成初始化并准备好接受流量。
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
        summary="服务信息",
        description="获取服务信息。",
    )
    async def service_info() -> ServiceInfoResponse:
        """
        服务信息端点。
        
        返回服务的相关信息。
        """
        info = health_service.get_service_info()
        return ServiceInfoResponse(**info)
    
    return router
