"""端口定义 - 入站和出站接口"""
from abc import ABC, abstractmethod
from typing import Optional, BinaryIO
from dataclasses import dataclass

from domain.entities import App, AppPackage, PublishStatus


# ============ 出站端口（被驱动端口）============

class IAppRepository(ABC):
    """应用仓储端口"""
    
    @abstractmethod
    async def find_by_id(self, app_id: int) -> Optional[App]:
        """根据ID查找应用"""
        pass
    
    @abstractmethod
    async def find_all(
        self,
        publish_status: Optional[PublishStatus] = None,
        include_deleted: bool = False,
    ) -> list[App]:
        """查找所有应用"""
        pass
    
    @abstractmethod
    async def save(self, app: App) -> App:
        """保存应用（创建或更新）"""
        pass
    
    @abstractmethod
    async def delete(self, app_id: int) -> None:
        """删除应用"""
        pass


class IAppPackageRepository(ABC):
    """应用包仓储端口"""
    
    @abstractmethod
    async def find_by_id(self, package_id: int) -> Optional[AppPackage]:
        """根据ID查找应用包"""
        pass
    
    @abstractmethod
    async def find_by_app_id(self, app_id: int, limit: int = 10) -> list[AppPackage]:
        """根据应用ID查找应用包列表"""
        pass
    
    @abstractmethod
    async def find_latest_by_app_id(self, app_id: int) -> Optional[AppPackage]:
        """查找应用最新的包"""
        pass
    
    @abstractmethod
    async def save(self, package: AppPackage) -> AppPackage:
        """保存应用包"""
        pass


@dataclass
class PackageManifest:
    """应用包清单"""
    manifest_version: int
    name: str
    version: str


@dataclass
class ProtonUploadResult:
    """Proton上传结果"""
    chart_code: str
    image_code: str


class IPackageParser(ABC):
    """应用包解析器端口"""
    
    @abstractmethod
    async def parse(self, file: BinaryIO) -> PackageManifest:
        """解析ZIP包并验证，返回manifest信息"""
        pass
    
    @abstractmethod
    async def extract_chart(self, file: BinaryIO) -> bytes:
        """从ZIP包中提取chart"""
        pass


class IProtonService(ABC):
    """Proton服务端口（外部服务）"""
    
    @abstractmethod
    async def upload_package(self, chart_data: bytes, image_data: bytes) -> ProtonUploadResult:
        """上传应用包到Proton"""
        pass

