"""FastAPI 依赖注入"""
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends, Header

from infrastructure.config import Settings, get_settings
from infrastructure.persistence.repositories import AppRepository, AppPackageRepository
from infrastructure.external.proton_service import ProtonService
from infrastructure.external.package_parser import ZipPackageParser
from application.services import AppService


# 单例实例
_app_repository: Optional[AppRepository] = None
_package_repository: Optional[AppPackageRepository] = None
_proton_service: Optional[ProtonService] = None
_package_parser: Optional[ZipPackageParser] = None


def reset_singletons():
    """重置所有单例（测试用）"""
    global _app_repository, _package_repository, _proton_service, _package_parser
    _app_repository = None
    _package_repository = None
    _proton_service = None
    _package_parser = None


def get_app_repository() -> AppRepository:
    """获取应用仓储实例（单例）"""
    global _app_repository
    if _app_repository is None:
        _app_repository = AppRepository()
    return _app_repository


def get_package_repository() -> AppPackageRepository:
    """获取应用包仓储实例（单例）"""
    global _package_repository
    if _package_repository is None:
        _package_repository = AppPackageRepository()
    return _package_repository


def get_proton_service() -> ProtonService:
    """获取Proton服务实例（单例）"""
    global _proton_service
    if _proton_service is None:
        settings = get_settings()
        _proton_service = ProtonService(base_url=settings.proton_service_url)
    return _proton_service


def get_package_parser() -> ZipPackageParser:
    """获取包解析器实例（单例）"""
    global _package_parser
    if _package_parser is None:
        _package_parser = ZipPackageParser()
    return _package_parser


def get_app_service(
    app_repository: Annotated[AppRepository, Depends(get_app_repository)],
    package_repository: Annotated[AppPackageRepository, Depends(get_package_repository)],
    proton_service: Annotated[ProtonService, Depends(get_proton_service)],
    package_parser: Annotated[ZipPackageParser, Depends(get_package_parser)],
) -> AppService:
    """获取应用服务实例"""
    return AppService(
        app_repository=app_repository,
        package_repository=package_repository,
        proton_service=proton_service,
        package_parser=package_parser,
    )


def get_current_user_id(
    x_user_id: Annotated[str, Header(alias="X-User-Id")] = "anonymous"
) -> str:
    """从请求头获取当前用户ID"""
    return x_user_id


# 类型别名
AppServiceDep = Annotated[AppService, Depends(get_app_service)]
CurrentUserDep = Annotated[str, Depends(get_current_user_id)]

