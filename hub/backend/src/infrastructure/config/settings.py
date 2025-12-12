"""
应用配置管理

使用 pydantic-settings 进行配置管理。
配置可以通过环境变量或 .env 文件进行设置。
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置。
    
    所有配置都可以通过环境变量进行设置。
    环境变量需要以 'DIP_HUB_' 为前缀。
    """
    
    model_config = SettingsConfigDict(
        env_prefix="DIP_HUB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # 应用配置
    app_name: str = Field(default="DIP Hub", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    
    # 服务器配置
    host: str = Field(default="0.0.0.0", description="服务器监听地址")
    port: int = Field(default=8000, description="服务器监听端口")
    workers: int = Field(default=1, description="工作进程数")
    
    # API 配置
    api_prefix: str = Field(default="/api/internal/dip-hub/v1", description="API 前缀")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式"
    )
    
    # 健康检查配置
    health_check_timeout: int = Field(default=5, description="健康检查超时时间（秒）")


@lru_cache
def get_settings() -> Settings:
    """
    获取缓存的配置实例。
    
    返回:
        Settings: 应用配置。
    """
    return Settings()
