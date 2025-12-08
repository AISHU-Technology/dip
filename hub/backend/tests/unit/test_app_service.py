"""应用服务单元测试"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import io

from domain.entities import App, AppPackage, DevMode, PublishStatus
from domain.exceptions import (
    AppNotFoundException,
    AppCannotBePublishedException,
    AppNotPublishedException,
)
from application.dto import CreateAppDto, UpdateAppDto
from application.services import AppService


class TestAppServiceCreateApp:
    """创建应用测试"""
    
    @pytest.mark.asyncio
    async def test_create_app_success(self, app_service, mock_app_repository):
        """测试成功创建应用"""
        dto = CreateAppDto(
            name="Test App",
            description="Test description",
            dev_mode=1,
        )
        
        # Mock保存后返回带ID的应用
        async def save_app(app):
            app.id = 1
            return app
        mock_app_repository.save.side_effect = save_app
        
        result = await app_service.create_app(dto, "user-001")
        
        assert result.id == 1
        mock_app_repository.save.assert_called_once()
        
        # 验证传入的应用属性
        saved_app = mock_app_repository.save.call_args[0][0]
        assert saved_app.name == "Test App"
        assert saved_app.creator_id == "user-001"
        assert saved_app.editor_id == "user-001"
        assert saved_app.publish_status == PublishStatus.UNPUBLISHED
    
    @pytest.mark.asyncio
    async def test_create_app_minimal(self, app_service, mock_app_repository):
        """测试创建应用（最小参数）"""
        dto = CreateAppDto(name="Minimal")
        
        async def save_app(app):
            app.id = 2
            return app
        mock_app_repository.save.side_effect = save_app
        
        result = await app_service.create_app(dto, "user-002")
        
        assert result.id == 2


class TestAppServiceUpdateApp:
    """更新应用测试"""
    
    @pytest.mark.asyncio
    async def test_update_app_success(self, app_service, mock_app_repository, sample_app):
        """测试成功更新应用"""
        sample_app.id = 1
        mock_app_repository.find_by_id.return_value = sample_app
        
        dto = UpdateAppDto(name="Updated Name", description="Updated desc")
        
        result = await app_service.update_app(1, dto, "user-002")
        
        assert result.success is True
        mock_app_repository.save.assert_called_once()
        
        # 验证更新后的属性
        assert sample_app.name == "Updated Name"
        assert sample_app.description == "Updated desc"
        assert sample_app.editor_id == "user-002"
    
    @pytest.mark.asyncio
    async def test_update_app_not_found(self, app_service, mock_app_repository):
        """测试更新不存在的应用"""
        mock_app_repository.find_by_id.return_value = None
        
        dto = UpdateAppDto(name="New Name")
        
        with pytest.raises(AppNotFoundException):
            await app_service.update_app(999, dto, "user-001")
    
    @pytest.mark.asyncio
    async def test_update_deleted_app(self, app_service, mock_app_repository, sample_app):
        """测试更新已删除的应用"""
        sample_app.id = 1
        sample_app.is_deleted = True
        mock_app_repository.find_by_id.return_value = sample_app
        
        dto = UpdateAppDto(name="New Name")
        
        with pytest.raises(AppNotFoundException):
            await app_service.update_app(1, dto, "user-001")


class TestAppServiceListApps:
    """应用列表测试"""
    
    @pytest.mark.asyncio
    async def test_list_apps_all(self, app_service, mock_app_repository):
        """测试获取所有应用"""
        apps = [
            App.create(name="App 1", creator_id="user-001"),
            App.create(name="App 2", creator_id="user-001"),
        ]
        apps[0].id = 1
        apps[1].id = 2
        mock_app_repository.find_all.return_value = apps
        
        result = await app_service.list_apps()
        
        assert len(result) == 2
        mock_app_repository.find_all.assert_called_once_with(publish_status=None)
    
    @pytest.mark.asyncio
    async def test_list_apps_filter_by_status(self, app_service, mock_app_repository):
        """测试按发布状态过滤应用"""
        apps = [App.create(name="Published", creator_id="user-001")]
        apps[0].id = 1
        apps[0].publish_status = PublishStatus.PUBLISHED
        mock_app_repository.find_all.return_value = apps
        
        result = await app_service.list_apps(publish_status=1)
        
        assert len(result) == 1
        mock_app_repository.find_all.assert_called_once_with(
            publish_status=PublishStatus.PUBLISHED
        )


class TestAppServiceGetAppDetail:
    """应用详情测试"""
    
    @pytest.mark.asyncio
    async def test_get_app_detail_success(
        self, app_service, mock_app_repository, mock_package_repository, sample_app, sample_package
    ):
        """测试获取应用详情"""
        sample_app.id = 1
        sample_package.id = 100
        
        mock_app_repository.find_by_id.return_value = sample_app
        mock_package_repository.find_by_app_id.return_value = [sample_package]
        
        result = await app_service.get_app_detail(1)
        
        assert result.id == 1
        assert result.name == sample_app.name
        assert len(result.app_packages) == 1
        assert result.app_packages[0].package_id == 100
    
    @pytest.mark.asyncio
    async def test_get_app_detail_not_found(self, app_service, mock_app_repository):
        """测试获取不存在的应用详情"""
        mock_app_repository.find_by_id.return_value = None
        
        with pytest.raises(AppNotFoundException):
            await app_service.get_app_detail(999)


class TestAppServicePublish:
    """发布应用测试"""
    
    @pytest.mark.asyncio
    async def test_publish_app_success(
        self, app_service, mock_app_repository, mock_package_repository, sample_app, sample_package
    ):
        """测试成功发布应用"""
        sample_app.id = 1
        sample_app.publish_status = PublishStatus.UNPUBLISHED
        sample_package.id = 100
        
        mock_app_repository.find_by_id.return_value = sample_app
        mock_package_repository.find_latest_by_app_id.return_value = sample_package
        
        result = await app_service.publish_app(1, "user-001")
        
        assert result.success is True
        assert sample_app.publish_status == PublishStatus.PUBLISHED
        assert sample_app.release_app_package_id == 100
    
    @pytest.mark.asyncio
    async def test_publish_app_already_published(
        self, app_service, mock_app_repository, sample_published_app
    ):
        """测试发布已发布的应用"""
        mock_app_repository.find_by_id.return_value = sample_published_app
        
        with pytest.raises(AppCannotBePublishedException):
            await app_service.publish_app(1, "user-001")
    
    @pytest.mark.asyncio
    async def test_publish_app_no_package(
        self, app_service, mock_app_repository, mock_package_repository, sample_app
    ):
        """测试发布没有包的应用"""
        sample_app.id = 1
        mock_app_repository.find_by_id.return_value = sample_app
        mock_package_repository.find_latest_by_app_id.return_value = None
        
        with pytest.raises(AppCannotBePublishedException):
            await app_service.publish_app(1, "user-001")


class TestAppServiceUnpublish:
    """撤销发布测试"""
    
    @pytest.mark.asyncio
    async def test_unpublish_app_success(
        self, app_service, mock_app_repository, sample_published_app
    ):
        """测试成功撤销发布"""
        mock_app_repository.find_by_id.return_value = sample_published_app
        
        result = await app_service.unpublish_app(1, "user-001")
        
        assert result.success is True
        assert sample_published_app.publish_status == PublishStatus.UNPUBLISHED
    
    @pytest.mark.asyncio
    async def test_unpublish_app_not_published(
        self, app_service, mock_app_repository, sample_app
    ):
        """测试撤销未发布的应用"""
        sample_app.id = 1
        mock_app_repository.find_by_id.return_value = sample_app
        
        with pytest.raises(AppNotPublishedException):
            await app_service.unpublish_app(1, "user-001")


class TestAppServiceDelete:
    """删除应用测试"""
    
    @pytest.mark.asyncio
    async def test_delete_app_success(self, app_service, mock_app_repository, sample_app):
        """测试成功删除应用"""
        sample_app.id = 1
        mock_app_repository.find_by_id.return_value = sample_app
        
        result = await app_service.delete_app(1, "user-001")
        
        assert result.success is True
        assert sample_app.is_deleted is True
    
    @pytest.mark.asyncio
    async def test_delete_app_not_found(self, app_service, mock_app_repository):
        """测试删除不存在的应用"""
        mock_app_repository.find_by_id.return_value = None
        
        with pytest.raises(AppNotFoundException):
            await app_service.delete_app(999, "user-001")


class TestAppServiceUploadPackage:
    """上传应用包测试"""
    
    @pytest.mark.asyncio
    async def test_upload_package_success(
        self,
        app_service,
        mock_app_repository,
        mock_package_repository,
        mock_proton_service,
        mock_package_parser,
        sample_app,
    ):
        """测试成功上传应用包"""
        sample_app.id = 1
        mock_app_repository.find_by_id.return_value = sample_app
        
        async def save_package(pkg):
            pkg.id = 100
            return pkg
        mock_package_repository.save.side_effect = save_package
        
        file = io.BytesIO(b"zip-content")
        
        result = await app_service.upload_package(1, file, "user-001")
        
        assert result.id == 100
        mock_package_parser.parse.assert_called_once()
        mock_proton_service.upload_package.assert_called_once()
        mock_package_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_upload_package_app_not_found(
        self, app_service, mock_app_repository
    ):
        """测试上传包到不存在的应用"""
        mock_app_repository.find_by_id.return_value = None
        
        file = io.BytesIO(b"zip-content")
        
        with pytest.raises(AppNotFoundException):
            await app_service.upload_package(999, file, "user-001")

