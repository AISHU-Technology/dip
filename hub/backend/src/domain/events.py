"""领域事件定义"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DomainEvent:
    """领域事件基类"""
    occurred_at: datetime


@dataclass(frozen=True)
class AppCreatedEvent(DomainEvent):
    """应用创建事件"""
    app_id: int
    name: str
    creator_id: str


@dataclass(frozen=True)
class AppPublishedEvent(DomainEvent):
    """应用发布事件"""
    app_id: int
    package_id: int


@dataclass(frozen=True)
class AppUnpublishedEvent(DomainEvent):
    """应用撤销发布事件"""
    app_id: int


@dataclass(frozen=True)
class PackageUploadedEvent(DomainEvent):
    """应用包上传事件"""
    app_id: int
    package_id: int
    package_name: str
    upload_user_id: str


@dataclass(frozen=True)
class AppDeletedEvent(DomainEvent):
    """应用删除事件"""
    app_id: int

