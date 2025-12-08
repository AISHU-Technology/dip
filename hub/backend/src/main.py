"""应用入口"""
import sys
from pathlib import Path

# 将src目录添加到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config import get_settings
from infrastructure.api.routes import router
from domain.exceptions import DomainException, AppNotFoundException

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="应用管理模块 - 管理DIP应用的全生命周期",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """领域异常处理器"""
    status_code = 400
    if isinstance(exc, AppNotFoundException):
        status_code = 404
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc) if settings.debug else "Internal server error",
            }
        },
    )


# 注册路由
app.include_router(router, prefix=settings.api_prefix)


@app.get("/health", tags=["health"])
async def health_check():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )

