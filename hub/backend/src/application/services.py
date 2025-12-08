"""应用服务 - 用例实现"""
from dataclasses import dataclass
from typing import Optional, BinaryIO

from domain.entities import App, AppPackage, DevMode, PublishStatus
from domain.exceptions import (
    AppNotFoundException,
    AppCannotBePublishedException,
    AppNotPublishedException,
    InvalidPackageException,
)
from application.ports import (
    IAppRepository,
    IAppPackageRepository,
    IProtonService,
    IPackageParser,
)
from application.dto import (
    CreateAppDto,
    UpdateAppDto,
    AppResponseDto,
    AppDetailResponseDto,
    CreateAppResponseDto,
    SuccessResponseDto,
)
from application.mappers import AppMapper


@dataclass
class AppService:
    """应用管理服务"""
    
    app_repository: IAppRepository
    package_repository: IAppPackageRepository
    proton_service: IProtonService
    package_parser: IPackageParser
    
    async def create_app(self, dto: CreateAppDto, user_id: str) -> CreateAppResponseDto:
        """
        创建应用
        
        业务规则：
        - 创建后 editor = creator
        - publish_status = 0 (未发布)
        - 开发模式不可修改，目前只支持上传模式
        """
        app = App.create(
            name=dto.name,
            creator_id=user_id,
            dev_mode=DevMode(dto.dev_mode),
            description=dto.description,
            cover_base64=dto.cover_base64,
        )
        
        saved_app = await self.app_repository.save(app)
        return CreateAppResponseDto(id=saved_app.id)
    
    async def upload_package(
        self,
        app_id: int,
        file: BinaryIO,
        user_id: str,
    ) -> CreateAppResponseDto:
        """
        上传应用包
        
        业务验证：
        - ZIP必须包含manifest.json
        - 记录版本信息
        - 更新publish_status = 2 (未发布更新)
        """
        # 1. 查找应用
        app = await self.app_repository.find_by_id(app_id)
        if not app or app.is_deleted:
            raise AppNotFoundException(app_id)
        
        # 2. 解析ZIP包
        try:
            manifest = await self.package_parser.parse(file)
        except Exception as e:
            raise InvalidPackageException(str(e))
        
        # 3. 提取chart并上传到Proton
        file.seek(0)  # 重置文件指针
        chart_data = await self.package_parser.extract_chart(file)
        proton_result = await self.proton_service.upload_package(chart_data, b"")
        
        # 4. 创建应用包记录
        package = AppPackage.create(
            app_id=app_id,
            name=manifest.name,
            proton_chart_code=proton_result.chart_code,
            proton_image_code=proton_result.image_code,
            upload_user_id=user_id,
        )
        saved_package = await self.package_repository.save(package)
        
        # 5. 更新应用状态
        app.mark_as_unpublished_update()
        app.editor_id = user_id
        await self.app_repository.save(app)
        
        return CreateAppResponseDto(id=saved_package.id)
    
    async def update_app(
        self,
        app_id: int,
        dto: UpdateAppDto,
        user_id: str,
    ) -> SuccessResponseDto:
        """
        编辑应用（名称/描述/封面）
        
        业务检查：
        - 只能修改名称/描述/封面
        - 修改后更新editorId和editTime
        """
        app = await self.app_repository.find_by_id(app_id)
        if not app or app.is_deleted:
            raise AppNotFoundException(app_id)
        
        app.update_metadata(
            editor_id=user_id,
            name=dto.name,
            description=dto.description,
            cover_base64=dto.cover_base64,
        )
        
        await self.app_repository.save(app)
        return SuccessResponseDto(success=True)
    
    async def list_apps(
        self,
        publish_status: Optional[int] = None,
    ) -> list[AppResponseDto]:
        """
        浏览应用列表
        
        排序逻辑：
        - 后端默认按edit_time DESC
        """
        status = PublishStatus(publish_status) if publish_status is not None else None
        apps = await self.app_repository.find_all(publish_status=status)
        
        # 按edit_time降序排序
        apps.sort(key=lambda x: x.edit_time, reverse=True)
        
        return [AppMapper.to_response_dto(app) for app in apps]
    
    async def get_app_detail(self, app_id: int) -> AppDetailResponseDto:
        """
        查看应用详情
        
        包括：
        - 应用元数据
        - 最近10个版本的应用安装包（按upload_time倒序）
        """
        app = await self.app_repository.find_by_id(app_id)
        if not app or app.is_deleted:
            raise AppNotFoundException(app_id)
        
        # 获取最近10个包
        packages = await self.package_repository.find_by_app_id(app_id, limit=10)
        
        return AppMapper.to_detail_dto(app, packages)
    
    async def publish_app(self, app_id: int, user_id: str) -> SuccessResponseDto:
        """
        发布应用
        
        业务逻辑：
        - 只有状态为未发布或未发布更新可发布
        - 发布成功后publish_status = 1
        - 将最新包标记为release_app_package_id
        """
        app = await self.app_repository.find_by_id(app_id)
        if not app or app.is_deleted:
            raise AppNotFoundException(app_id)
        
        if not app.can_publish():
            raise AppCannotBePublishedException(app_id, "App is already published")
        
        # 获取最新的包
        latest_package = await self.package_repository.find_latest_by_app_id(app_id)
        if not latest_package:
            raise AppCannotBePublishedException(app_id, "No package uploaded")
        
        app.publish(latest_package.id)
        app.editor_id = user_id
        await self.app_repository.save(app)
        
        return SuccessResponseDto(success=True)
    
    async def unpublish_app(self, app_id: int, user_id: str) -> SuccessResponseDto:
        """
        撤销发布
        
        规则：
        - 只能撤销已发布状态应用
        - 不影响已安装的应用
        """
        app = await self.app_repository.find_by_id(app_id)
        if not app or app.is_deleted:
            raise AppNotFoundException(app_id)
        
        if app.publish_status != PublishStatus.PUBLISHED:
            raise AppNotPublishedException(app_id)
        
        app.unpublish()
        app.editor_id = user_id
        await self.app_repository.save(app)
        
        return SuccessResponseDto(success=True)
    
    async def delete_app(self, app_id: int, user_id: str) -> SuccessResponseDto:
        """
        删除应用
        
        规则：
        - 删除后标记is_deleted = 1
        - 不影响已安装应用
        """
        app = await self.app_repository.find_by_id(app_id)
        if not app or app.is_deleted:
            raise AppNotFoundException(app_id)
        
        app.soft_delete()
        app.editor_id = user_id
        await self.app_repository.save(app)
        
        return SuccessResponseDto(success=True)

