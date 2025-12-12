"""
依赖注入容器

按照六边形架构组装和连接所有依赖。
在这里实例化适配器并注入到应用服务中。
"""
from src.application.health_service import HealthService
from src.adapters.health_adapter import HealthAdapter
from src.infrastructure.config.settings import Settings, get_settings


class Container:
    """
    依赖注入容器。
    
    该容器负责组装所有依赖，并提供工厂方法来创建带有适配器的应用服务。
    """
    
    def __init__(self, settings: Settings = None):
        """
        初始化容器。
        
        参数:
            settings: 应用配置。如果为 None，则使用默认配置。
        """
        self._settings = settings or get_settings()
        self._health_adapter = None
        self._health_service = None
    
    @property
    def settings(self) -> Settings:
        """获取应用配置。"""
        return self._settings
    
    @property
    def health_adapter(self) -> HealthAdapter:
        """获取健康适配器实例（单例）。"""
        if self._health_adapter is None:
            self._health_adapter = HealthAdapter(self._settings)
        return self._health_adapter
    
    @property
    def health_service(self) -> HealthService:
        """获取健康服务实例（单例）。"""
        if self._health_service is None:
            self._health_service = HealthService(self.health_adapter)
        return self._health_service
    
    def set_ready(self, ready: bool = True) -> None:
        """
        设置服务就绪状态。
        
        参数:
            ready: 服务是否就绪。
        """
        self.health_adapter.set_ready(ready)


# 全局容器实例
_container: Container = None


def get_container() -> Container:
    """
    获取全局容器实例。
    
    返回:
        Container: 容器实例。
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def init_container(settings: Settings = None) -> Container:
    """
    初始化全局容器。
    
    参数:
        settings: 应用配置。
    
    返回:
        Container: 初始化后的容器。
    """
    global _container
    _container = Container(settings)
    return _container
