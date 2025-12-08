"""领域实体单元测试"""
import pytest
from datetime import datetime

from domain.entities import App, AppPackage, DevMode, PublishStatus


class TestApp:
    """App实体测试"""
    
    def test_create_app(self):
        """测试创建应用"""
        app = App.create(
            name="Test App",
            creator_id="user-001",
            dev_mode=DevMode.UPLOAD,
            description="Test description",
            cover_base64="base64data",
        )
        
        assert app.id is None
        assert app.name == "Test App"
        assert app.creator_id == "user-001"
        assert app.editor_id == "user-001"  # 创建时editor = creator
        assert app.dev_mode == DevMode.UPLOAD
        assert app.publish_status == PublishStatus.UNPUBLISHED
        assert app.release_app_package_id == 0
        assert app.is_deleted is False
        assert app.description == "Test description"
        assert app.cover_base64 == "base64data"
    
    def test_create_app_minimal(self):
        """测试创建应用（最小参数）"""
        app = App.create(
            name="Minimal App",
            creator_id="user-002",
        )
        
        assert app.name == "Minimal App"
        assert app.description is None
        assert app.cover_base64 is None
        assert app.dev_mode == DevMode.UPLOAD  # 默认值
    
    def test_update_metadata(self):
        """测试更新应用元数据"""
        app = App.create(name="Old Name", creator_id="user-001")
        old_edit_time = app.edit_time
        
        app.update_metadata(
            editor_id="user-002",
            name="New Name",
            description="New description",
        )
        
        assert app.name == "New Name"
        assert app.description == "New description"
        assert app.editor_id == "user-002"
        assert app.edit_time >= old_edit_time
    
    def test_update_metadata_partial(self):
        """测试部分更新元数据"""
        app = App.create(
            name="Original",
            creator_id="user-001",
            description="Original desc",
        )
        
        app.update_metadata(editor_id="user-002", name="Updated")
        
        assert app.name == "Updated"
        assert app.description == "Original desc"  # 未改变
    
    def test_can_publish_unpublished(self):
        """测试未发布状态可以发布"""
        app = App.create(name="Test", creator_id="user-001")
        app.publish_status = PublishStatus.UNPUBLISHED
        
        assert app.can_publish() is True
    
    def test_can_publish_unpublished_update(self):
        """测试未发布更新状态可以发布"""
        app = App.create(name="Test", creator_id="user-001")
        app.publish_status = PublishStatus.UNPUBLISHED_UPDATE
        
        assert app.can_publish() is True
    
    def test_cannot_publish_already_published(self):
        """测试已发布状态不能再次发布"""
        app = App.create(name="Test", creator_id="user-001")
        app.publish_status = PublishStatus.PUBLISHED
        
        assert app.can_publish() is False
    
    def test_publish(self):
        """测试发布应用"""
        app = App.create(name="Test", creator_id="user-001")
        
        app.publish(package_id=100)
        
        assert app.publish_status == PublishStatus.PUBLISHED
        assert app.release_app_package_id == 100
    
    def test_unpublish(self):
        """测试撤销发布"""
        app = App.create(name="Test", creator_id="user-001")
        app.publish(package_id=100)
        
        app.unpublish()
        
        assert app.publish_status == PublishStatus.UNPUBLISHED
    
    def test_mark_as_unpublished_update(self):
        """测试标记为未发布更新"""
        app = App.create(name="Test", creator_id="user-001")
        app.publish_status = PublishStatus.PUBLISHED
        
        app.mark_as_unpublished_update()
        
        assert app.publish_status == PublishStatus.UNPUBLISHED_UPDATE
    
    def test_mark_as_unpublished_update_when_not_published(self):
        """测试未发布时标记为未发布更新（状态不变）"""
        app = App.create(name="Test", creator_id="user-001")
        app.publish_status = PublishStatus.UNPUBLISHED
        
        app.mark_as_unpublished_update()
        
        # 未发布状态不变
        assert app.publish_status == PublishStatus.UNPUBLISHED
    
    def test_soft_delete(self):
        """测试软删除"""
        app = App.create(name="Test", creator_id="user-001")
        
        app.soft_delete()
        
        assert app.is_deleted is True


class TestAppPackage:
    """AppPackage实体测试"""
    
    def test_create_package(self):
        """测试创建应用包"""
        package = AppPackage.create(
            app_id=1,
            name="test-package",
            proton_chart_code="chart-123",
            proton_image_code="image-456",
            upload_user_id="user-001",
        )
        
        assert package.id is None
        assert package.app_id == 1
        assert package.name == "test-package"
        assert package.proton_chart_code == "chart-123"
        assert package.proton_image_code == "image-456"
        assert package.upload_user_id == "user-001"
        assert isinstance(package.upload_time, datetime)

