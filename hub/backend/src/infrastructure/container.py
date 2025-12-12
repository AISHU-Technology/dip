"""
Dependency Injection Container

Assembles and wires all dependencies following the hexagonal architecture.
This is where adapters are instantiated and injected into application services.
"""
from src.application.health_service import HealthService
from src.adapters.health_adapter import HealthAdapter
from src.infrastructure.config.settings import Settings, get_settings


class Container:
    """
    Dependency injection container.
    
    This container assembles all the dependencies and provides
    factory methods to create application services with their adapters.
    """
    
    def __init__(self, settings: Settings = None):
        """
        Initialize the container.
        
        Args:
            settings: Application settings. If None, uses default settings.
        """
        self._settings = settings or get_settings()
        self._health_adapter = None
        self._health_service = None
    
    @property
    def settings(self) -> Settings:
        """Get the application settings."""
        return self._settings
    
    @property
    def health_adapter(self) -> HealthAdapter:
        """Get the health adapter instance (singleton)."""
        if self._health_adapter is None:
            self._health_adapter = HealthAdapter(self._settings)
        return self._health_adapter
    
    @property
    def health_service(self) -> HealthService:
        """Get the health service instance (singleton)."""
        if self._health_service is None:
            self._health_service = HealthService(self.health_adapter)
        return self._health_service
    
    def set_ready(self, ready: bool = True) -> None:
        """
        Set the service ready status.
        
        Args:
            ready: Whether the service is ready.
        """
        self.health_adapter.set_ready(ready)


# Global container instance
_container: Container = None


def get_container() -> Container:
    """
    Get the global container instance.
    
    Returns:
        Container: The container instance.
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def init_container(settings: Settings = None) -> Container:
    """
    Initialize the global container.
    
    Args:
        settings: Application settings.
    
    Returns:
        Container: The initialized container.
    """
    global _container
    _container = Container(settings)
    return _container

