"""
应用 API Schema

定义应用相关的 API 请求和响应模型。
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ApplicationConfigOntology(BaseModel):
    """
    业务知识网络配置模型。

    属性:
        id: 业务知识网络 ID
    """
    id: str = Field(..., description="业务知识网络 ID")


class ApplicationConfigAgent(BaseModel):
    """
    智能体配置模型。

    属性:
        id: Data Agent 智能体 ID
    """
    id: str = Field(..., description="Data Agent 智能体 ID")


class ApplicationConfig(BaseModel):
    """
    应用配置模型。

    属性:
        ontologies: 业务知识网络配置列表
        agents: Data Agent 智能体配置列表
    """
    ontologies: Optional[List[ApplicationConfigOntology]] = Field(
        None,
        description="业务知识网络配置"
    )
    agents: Optional[List[ApplicationConfigAgent]] = Field(
        None,
        description="Data Agent 智能体配置"
    )


class ApplicationResponse(BaseModel):
    """
    应用响应模型。

    属性:
        key: 应用包唯一标识
        name: 应用名称
        description: 应用描述
        version: 当前版本号
        icon: 应用图标，Base64编码
        category: 应用所属分类
        updated_by: 更新者用户 ID
        updated_at: 更新时间
    """
    key: str = Field(..., description="应用包唯一标识")
    name: str = Field(..., description="应用名称")
    description: Optional[str] = Field(None, description="应用描述")
    version: Optional[str] = Field(None, description="当前版本号")
    icon: Optional[str] = Field(None, description="应用图标，Base64编码")
    category: Optional[str] = Field(None, description="应用所属分类")
    updated_by: str = Field(..., description="更新者用户 ID")
    updated_at: datetime = Field(..., description="更新时间")


# ApplicationListResponse: 应用列表响应是一个数组，类型为 List[ApplicationResponse]


class CreateApplicationRequest(BaseModel):
    """
    创建应用请求模型。

    属性:
        key: 应用包唯一标识
        name: 应用名称
        description: 应用描述
        version: 当前版本号
        config: 应用配置
        updated_by: 更新者用户 ID
    """
    key: str = Field(..., description="应用包唯一标识", min_length=1, max_length=32)
    name: str = Field(..., description="应用名称", min_length=1, max_length=128)
    description: Optional[str] = Field(None, description="应用描述", max_length=800)
    version: Optional[str] = Field(None, description="当前版本号", max_length=128)
    config: Optional[Dict[str, Any]] = Field(None, description="应用配置（JSON格式）")
    updated_by: str = Field(..., description="更新者用户 ID", min_length=1, max_length=36)


class UpdateApplicationRequest(BaseModel):
    """
    更新应用请求模型。

    属性:
        name: 应用名称
        description: 应用描述
        version: 当前版本号
        config: 应用配置
        updated_by: 更新者用户 ID
    """
    name: Optional[str] = Field(None, description="应用名称", min_length=1, max_length=128)
    description: Optional[str] = Field(None, description="应用描述", max_length=800)
    version: Optional[str] = Field(None, description="当前版本号", max_length=128)
    config: Optional[Dict[str, Any]] = Field(None, description="应用配置（JSON格式）")
    updated_by: str = Field(..., description="更新者用户 ID", min_length=1, max_length=36)
