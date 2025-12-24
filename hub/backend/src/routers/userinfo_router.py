"""
用户信息路由

用户信息端点的 FastAPI 路由。
这是处理 HTTP 请求并委托给应用层的接口适配器。
"""
import logging
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse

from src.application.user_info_service import UserInfoService

logger = logging.getLogger(__name__)


def create_userinfo_router(user_info_service: UserInfoService) -> APIRouter:
    """
    创建用户信息路由。

    参数:
        user_info_service: 用户信息服务实例

    返回:
        APIRouter: 配置完成的路由
    """
    router = APIRouter(tags=["UserInfo"])

    @router.get(
        "/userinfo",
        summary="用户信息接口",
        description="用户信息接口，根据 Token 获取用户信息",
    )
    async def userinfo(request: Request):
        """
        用户信息接口。

        流程：
        1. 从 Authorization Header 获取 Token
        2. 获取用户信息
        3. 返回响应
        """
        try:
            # 获取 Token
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Authorization Header 格式错误",
                )
            
            token = auth_header[7:]  # 去除 "Bearer " 前缀

            # 获取用户信息
            user_info = await user_info_service.get_user_info(token)

            # 返回响应
            return JSONResponse(
                content={
                    "id": user_info.id,
                    "account": user_info.account,
                    "vision_name": user_info.vision_name,
                    "email": user_info.email,
                },
                status_code=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.error(f"获取用户信息失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"获取用户信息失败: {str(e)}",
            )
        except Exception as e:
            logger.exception(f"获取用户信息异常: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"获取用户信息失败: {str(e)}",
            )

    return router

