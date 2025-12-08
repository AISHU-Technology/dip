"""仓储实现 - 内存存储（用于开发和测试）"""
from typing import Optional
from datetime import datetime

from domain.entities import App, AppPackage, PublishStatus, DevMode
from application.ports import IAppRepository, IAppPackageRepository


class AppRepository(IAppRepository):
    """应用仓储实现（内存存储）"""
    
    def __init__(self):
        self._apps: dict[int, App] = {}
        self._id_counter = 1
    
    async def find_by_id(self, app_id: int) -> Optional[App]:
        """根据ID查找应用"""
        return self._apps.get(app_id)
    
    async def find_all(
        self,
        publish_status: Optional[PublishStatus] = None,
        include_deleted: bool = False,
    ) -> list[App]:
        """查找所有应用"""
        apps = list(self._apps.values())
        
        if not include_deleted:
            apps = [app for app in apps if not app.is_deleted]
        
        if publish_status is not None:
            apps = [app for app in apps if app.publish_status == publish_status]
        
        return apps
    
    async def save(self, app: App) -> App:
        """保存应用"""
        if app.id is None:
            app.id = self._id_counter
            self._id_counter += 1
        
        self._apps[app.id] = app
        return app
    
    async def delete(self, app_id: int) -> None:
        """删除应用"""
        if app_id in self._apps:
            del self._apps[app_id]
    
    def clear(self):
        """清空所有数据（测试用）"""
        self._apps.clear()
        self._id_counter = 1


class AppPackageRepository(IAppPackageRepository):
    """应用包仓储实现（内存存储）"""
    
    def __init__(self):
        self._packages: dict[int, AppPackage] = {}
        self._id_counter = 1
    
    async def find_by_id(self, package_id: int) -> Optional[AppPackage]:
        """根据ID查找应用包"""
        return self._packages.get(package_id)
    
    async def find_by_app_id(self, app_id: int, limit: int = 10) -> list[AppPackage]:
        """根据应用ID查找应用包列表"""
        packages = [
            pkg for pkg in self._packages.values()
            if pkg.app_id == app_id
        ]
        # 按upload_time降序排序
        packages.sort(key=lambda x: x.upload_time, reverse=True)
        return packages[:limit]
    
    async def find_latest_by_app_id(self, app_id: int) -> Optional[AppPackage]:
        """查找应用最新的包"""
        packages = await self.find_by_app_id(app_id, limit=1)
        return packages[0] if packages else None
    
    async def save(self, package: AppPackage) -> AppPackage:
        """保存应用包"""
        if package.id is None:
            package.id = self._id_counter
            self._id_counter += 1
        
        self._packages[package.id] = package
        return package
    
    def clear(self):
        """清空所有数据（测试用）"""
        self._packages.clear()
        self._id_counter = 1

