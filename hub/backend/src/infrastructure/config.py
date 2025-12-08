"""配置管理"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # 应用
    app_name: str = "App Management Hub"
    app_env: str = "development"
    debug: bool = False
    
    # 数据库 (MariaDB)
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/app_management"
    database_pool_size: int = 5
    
    # Proton 服务
    proton_service_url: str = "http://localhost:8080"
    
    # API
    api_prefix: str = "/dip/v1"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()

