"""
认证中间件

统一从请求头提取认证token并存储到request.state和TokenContext中，供后续处理使用。
同时进行token内省，获取用户信息并存储到上下文中。
"""
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.infrastructure.context.token_context import TokenContext, UserContext
from src.infrastructure.container import get_container

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    认证中间件。
    
    从请求头中提取Authorization token，进行内省验证，并存储到：
    1. request.state.auth_token - 供路由层使用
    2. TokenContext - 供适配器层统一获取
    3. UserContext - 供应用层统一获取用户信息
    
    如果请求头中没有Authorization，则auth_token为None。
    如果token无效或无法获取用户信息，则用户信息为None。
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        处理请求，提取认证token，进行内省并获取用户信息。
        
        参数:
            request: 请求对象
            call_next: 下一个中间件或路由处理函数
        
        返回:
            Response: HTTP响应
        """
        # 从请求头提取Authorization token
        auth_header = request.headers.get("Authorization")
        auth_token = auth_header if auth_header else None
        
        # 存储到request.state中，供路由层使用
        request.state.auth_token = auth_token
        
        # 存储到TokenContext中，供适配器层统一获取
        TokenContext.set_token(auth_token)
        
        # 如果存在token，进行内省并获取用户信息
        user_info = None
        if auth_token:
            try:
                # 获取容器以访问适配器
                container = get_container()
                
                # 内省token获取用户ID
                introspect = await container.hydra_adapter.introspect(auth_token)
                if introspect.active and introspect.visitor_id:
                    # 获取用户详细信息
                    user_infos = await container.user_management_adapter.batch_get_user_info_by_id(
                        [introspect.visitor_id]
                    )
                    if introspect.visitor_id in user_infos:
                        user_info = user_infos[introspect.visitor_id]
                        logger.debug(f"用户信息已获取: {user_info.id} ({user_info.vision_name})")
                    else:
                        logger.warning(f"无法获取用户信息: {introspect.visitor_id}")
                else:
                    logger.debug("Token 内省结果：token 无效或无法获取用户ID")
            except Exception as e:
                # 内省失败不影响请求继续，只记录日志
                logger.warning(f"Token 内省失败: {e}", exc_info=True)
        
        # 存储用户信息到UserContext中，供应用层统一获取
        UserContext.set_user_info(user_info)
        
        try:
            # 继续处理请求
            response = await call_next(request)
            return response
        finally:
            # 请求处理完成后清除上下文，避免上下文污染
            TokenContext.clear_token()
            UserContext.clear_user_info()

