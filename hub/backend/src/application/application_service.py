"""
应用服务

应用层服务，负责编排应用管理操作。
该服务使用端口（接口），不依赖任何基础设施细节。
"""
from typing import List

from src.domains.application import Application
from src.ports.application_port import ApplicationPort


class ApplicationService:
    """
    应用服务。

    该服务属于应用层，通过端口编排应用管理的业务逻辑。
    """

    def __init__(self, application_port: ApplicationPort):
        """
        初始化应用服务。

        参数:
            application_port: 应用端口实现（注入的适配器）
        """
        self._application_port = application_port

    async def get_all_applications(self) -> List[Application]:
        """
        获取所有已安装的应用列表。

        返回:
            List[Application]: 应用列表
        """
        return await self._application_port.get_all_applications()

    async def get_application_by_key(self, key: str) -> Application:
        """
        根据应用唯一标识获取应用信息。

        参数:
            key: 应用包唯一标识

        返回:
            Application: 应用实体

        异常:
            ValueError: 当应用不存在时抛出
        """
        return await self._application_port.get_application_by_key(key)

    async def create_application(self, application: Application) -> Application:
        """
        创建新应用。

        参数:
            application: 应用实体

        返回:
            Application: 创建后的应用实体

        异常:
            ValueError: 当应用 key 已存在时抛出
        """
        return await self._application_port.create_application(application)

    async def update_application(self, application: Application) -> Application:
        """
        更新应用信息。

        参数:
            application: 应用实体

        返回:
            Application: 更新后的应用实体

        异常:
            ValueError: 当应用不存在时抛出
        """
        return await self._application_port.update_application(application)

    async def delete_application(self, key: str) -> bool:
        """
        删除应用。

        参数:
            key: 应用包唯一标识

        返回:
            bool: 是否删除成功

        异常:
            ValueError: 当应用不存在时抛出
        """
        return await self._application_port.delete_application(key)
