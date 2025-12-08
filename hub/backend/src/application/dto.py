"""数据传输对象定义"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============ Request DTOs ============

class CreateAppDto(BaseModel):
    """创建应用请求"""
    name: str = Field(..., min_length=1, max_length=128, description="应用名称")
    description: Optional[str] = Field(None, max_length=800, description="应用描述")
    cover_base64: Optional[str] = Field(None, description="封面图片Base64")
    dev_mode: int = Field(1, description="开发模式：1=上传, 2=在线开发")


class UpdateAppDto(BaseModel):
    """更新应用请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=128, description="应用名称")
    description: Optional[str] = Field(None, max_length=800, description="应用描述")
    cover_base64: Optional[str] = Field(None, description="封面图片Base64")


# ============ Response DTOs ============

class CreateAppResponseDto(BaseModel):
    """创建应用响应"""
    id: int


class SuccessResponseDto(BaseModel):
    """通用成功响应"""
    success: bool = True


class AppResponseDto(BaseModel):
    """应用列表项响应"""
    id: int
    name: str
    description: Optional[str]
    cover_base64: Optional[str]
    editor: str = Field(..., description="编辑者ID")
    edit_time: datetime
    publish_status: int
    release_app_package_id: int
    
    model_config = {"from_attributes": True}


class AppPackageResponseDto(BaseModel):
    """应用包响应"""
    package_id: int = Field(..., alias="packageId")
    name: str
    upload_user_id: str
    upload_time: datetime
    
    model_config = {"from_attributes": True, "populate_by_name": True}


class AppDetailResponseDto(BaseModel):
    """应用详情响应"""
    id: int
    name: str
    description: Optional[str]
    cover_base64: Optional[str]
    creator: str
    create_time: datetime
    editor: str
    edit_time: datetime
    publish_status: int
    release_app_package_id: int
    app_packages: list[AppPackageResponseDto] = Field(default_factory=list, alias="app_package")
    
    model_config = {"from_attributes": True, "populate_by_name": True}


class PublishResultDto(BaseModel):
    """发布结果响应"""
    success: bool = True

