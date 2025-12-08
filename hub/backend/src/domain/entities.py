"""领域实体定义"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Optional


class PublishStatus(IntEnum):
    """发布状态枚举"""
    UNPUBLISHED = 0        # 未发布
    PUBLISHED = 1          # 已发布
    UNPUBLISHED_UPDATE = 2 # 未发布更新（有新版本待发布）


class DevMode(IntEnum):
    """开发模式枚举"""
    UPLOAD = 1   # 上传模式
    ONLINE = 2   # 在线开发模式（暂不支持）


@dataclass
class App:
    """应用领域实体"""
    id: Optional[int]
    name: str
    description: Optional[str]
    cover_base64: Optional[str]
    creator_id: str
    create_time: datetime
    editor_id: str
    edit_time: datetime
    dev_mode: DevMode
    publish_status: PublishStatus
    release_app_package_id: int = 0
    is_deleted: bool = False
    
    @classmethod
    def create(
        cls,
        name: str,
        creator_id: str,
        dev_mode: DevMode = DevMode.UPLOAD,
        description: Optional[str] = None,
        cover_base64: Optional[str] = None,
    ) -> "App":
        """工厂方法：创建新应用"""
        now = datetime.now()
        return cls(
            id=None,
            name=name,
            description=description,
            cover_base64=cover_base64,
            creator_id=creator_id,
            create_time=now,
            editor_id=creator_id,  # 创建时 editor = creator
            edit_time=now,
            dev_mode=dev_mode,
            publish_status=PublishStatus.UNPUBLISHED,
            release_app_package_id=0,
            is_deleted=False,
        )
    
    def update_metadata(
        self,
        editor_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        cover_base64: Optional[str] = None,
    ) -> None:
        """更新应用元数据（名称/描述/封面）"""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if cover_base64 is not None:
            self.cover_base64 = cover_base64
        self.editor_id = editor_id
        self.edit_time = datetime.now()
    
    def can_publish(self) -> bool:
        """检查是否可以发布"""
        # 只有未发布或未发布更新状态可以发布
        return self.publish_status in (PublishStatus.UNPUBLISHED, PublishStatus.UNPUBLISHED_UPDATE)
    
    def publish(self, package_id: int) -> None:
        """发布应用"""
        self.publish_status = PublishStatus.PUBLISHED
        self.release_app_package_id = package_id
        self.edit_time = datetime.now()
    
    def unpublish(self) -> None:
        """撤销发布"""
        self.publish_status = PublishStatus.UNPUBLISHED
        self.edit_time = datetime.now()
    
    def mark_as_unpublished_update(self) -> None:
        """标记为未发布更新（上传新包后）"""
        if self.publish_status == PublishStatus.PUBLISHED:
            self.publish_status = PublishStatus.UNPUBLISHED_UPDATE
        self.edit_time = datetime.now()
    
    def soft_delete(self) -> None:
        """软删除"""
        self.is_deleted = True
        self.edit_time = datetime.now()


@dataclass
class AppPackage:
    """应用包领域实体"""
    id: Optional[int]
    app_id: int
    name: str
    proton_chart_code: str
    proton_image_code: str
    upload_user_id: str
    upload_time: datetime
    
    @classmethod
    def create(
        cls,
        app_id: int,
        name: str,
        proton_chart_code: str,
        proton_image_code: str,
        upload_user_id: str,
    ) -> "AppPackage":
        """工厂方法：创建新应用包"""
        return cls(
            id=None,
            app_id=app_id,
            name=name,
            proton_chart_code=proton_chart_code,
            proton_image_code=proton_image_code,
            upload_user_id=upload_user_id,
            upload_time=datetime.now(),
        )

