"""
应用领域模型

定义应用相关的领域模型和实体。
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Application:
    """
    应用领域模型。

    属性:
        id: 应用主键 ID
        key: 应用包唯一标识
        name: 应用名称
        description: 应用描述
        icon: 应用图标（Base64编码字符串）
        version: 当前版本号
        category: 应用所属分类
        config: 应用配置（JSON格式）
        updated_by: 更新者用户 ID
        updated_at: 更新时间
    """
    id: int
    key: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    version: Optional[str] = None
    category: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    updated_by: str = ""
    updated_at: Optional[datetime] = None

    def has_icon(self) -> bool:
        """
        检查应用是否有图标。

        返回:
            bool: 是否有图标
        """
        return self.icon is not None and len(self.icon) > 0

    def has_config(self) -> bool:
        """
        检查应用是否有配置。

        返回:
            bool: 是否有配置
        """
        return self.config is not None and len(self.config) > 0

    def get_ontology_ids(self) -> list[str]:
        """
        获取业务知识网络配置的 ID 列表。

        返回:
            list[str]: 业务知识网络 ID 列表
        """
        if not self.has_config():
            return []

        ontologies = self.config.get("ontologies", [])
        return [ont.get("id") for ont in ontologies if ont.get("id")]

    def get_agent_ids(self) -> list[str]:
        """
        获取智能体配置的 ID 列表。

        返回:
            list[str]: 智能体 ID 列表
        """
        if not self.has_config():
            return []

        agents = self.config.get("agents", [])
        return [agent.get("id") for agent in agents if agent.get("id")]
