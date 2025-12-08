"""仓储单元测试"""
import pytest

from domain.entities import App, AppPackage, DevMode, PublishStatus
from infrastructure.persistence.repositories import AppRepository, AppPackageRepository


class TestAppRepository:
    """应用仓储测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, memory_app_repository):
        """测试保存和查找应用"""
        app = App.create(name="Test App", creator_id="user-001")
        
        saved_app = await memory_app_repository.save(app)
        
        assert saved_app.id == 1
        
        found_app = await memory_app_repository.find_by_id(1)
        
        assert found_app is not None
        assert found_app.name == "Test App"
    
    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, memory_app_repository):
        """测试查找不存在的应用"""
        result = await memory_app_repository.find_by_id(999)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_find_all(self, memory_app_repository):
        """测试查找所有应用"""
        app1 = App.create(name="App 1", creator_id="user-001")
        app2 = App.create(name="App 2", creator_id="user-001")
        
        await memory_app_repository.save(app1)
        await memory_app_repository.save(app2)
        
        apps = await memory_app_repository.find_all()
        
        assert len(apps) == 2
    
    @pytest.mark.asyncio
    async def test_find_all_exclude_deleted(self, memory_app_repository):
        """测试查找所有应用（排除已删除）"""
        app1 = App.create(name="Active", creator_id="user-001")
        app2 = App.create(name="Deleted", creator_id="user-001")
        
        await memory_app_repository.save(app1)
        saved_app2 = await memory_app_repository.save(app2)
        saved_app2.soft_delete()
        
        apps = await memory_app_repository.find_all(include_deleted=False)
        
        assert len(apps) == 1
        assert apps[0].name == "Active"
    
    @pytest.mark.asyncio
    async def test_find_all_by_status(self, memory_app_repository):
        """测试按状态过滤应用"""
        app1 = App.create(name="Unpublished", creator_id="user-001")
        app2 = App.create(name="Published", creator_id="user-001")
        
        await memory_app_repository.save(app1)
        saved_app2 = await memory_app_repository.save(app2)
        saved_app2.publish_status = PublishStatus.PUBLISHED
        
        apps = await memory_app_repository.find_all(publish_status=PublishStatus.PUBLISHED)
        
        assert len(apps) == 1
        assert apps[0].name == "Published"
    
    @pytest.mark.asyncio
    async def test_update_app(self, memory_app_repository):
        """测试更新应用"""
        app = App.create(name="Original", creator_id="user-001")
        saved_app = await memory_app_repository.save(app)
        
        saved_app.update_metadata(editor_id="user-002", name="Updated")
        await memory_app_repository.save(saved_app)
        
        found_app = await memory_app_repository.find_by_id(saved_app.id)
        
        assert found_app.name == "Updated"
    
    @pytest.mark.asyncio
    async def test_delete_app(self, memory_app_repository):
        """测试删除应用"""
        app = App.create(name="To Delete", creator_id="user-001")
        saved_app = await memory_app_repository.save(app)
        
        await memory_app_repository.delete(saved_app.id)
        
        found_app = await memory_app_repository.find_by_id(saved_app.id)
        
        assert found_app is None


class TestAppPackageRepository:
    """应用包仓储测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, memory_package_repository):
        """测试保存和查找应用包"""
        package = AppPackage.create(
            app_id=1,
            name="test-package",
            proton_chart_code="chart-123",
            proton_image_code="image-456",
            upload_user_id="user-001",
        )
        
        saved_package = await memory_package_repository.save(package)
        
        assert saved_package.id == 1
        
        found_package = await memory_package_repository.find_by_id(1)
        
        assert found_package is not None
        assert found_package.name == "test-package"
    
    @pytest.mark.asyncio
    async def test_find_by_app_id(self, memory_package_repository):
        """测试根据应用ID查找包"""
        pkg1 = AppPackage.create(
            app_id=1, name="pkg1", proton_chart_code="c1",
            proton_image_code="i1", upload_user_id="user-001"
        )
        pkg2 = AppPackage.create(
            app_id=1, name="pkg2", proton_chart_code="c2",
            proton_image_code="i2", upload_user_id="user-001"
        )
        pkg3 = AppPackage.create(
            app_id=2, name="pkg3", proton_chart_code="c3",
            proton_image_code="i3", upload_user_id="user-001"
        )
        
        await memory_package_repository.save(pkg1)
        await memory_package_repository.save(pkg2)
        await memory_package_repository.save(pkg3)
        
        packages = await memory_package_repository.find_by_app_id(1)
        
        assert len(packages) == 2
    
    @pytest.mark.asyncio
    async def test_find_by_app_id_with_limit(self, memory_package_repository):
        """测试根据应用ID查找包（带限制）"""
        for i in range(5):
            pkg = AppPackage.create(
                app_id=1, name=f"pkg{i}", proton_chart_code=f"c{i}",
                proton_image_code=f"i{i}", upload_user_id="user-001"
            )
            await memory_package_repository.save(pkg)
        
        packages = await memory_package_repository.find_by_app_id(1, limit=3)
        
        assert len(packages) == 3
    
    @pytest.mark.asyncio
    async def test_find_latest_by_app_id(self, memory_package_repository):
        """测试查找最新的包"""
        pkg1 = AppPackage.create(
            app_id=1, name="old", proton_chart_code="c1",
            proton_image_code="i1", upload_user_id="user-001"
        )
        await memory_package_repository.save(pkg1)
        
        import time
        time.sleep(0.01)  # 确保时间戳不同
        
        pkg2 = AppPackage.create(
            app_id=1, name="new", proton_chart_code="c2",
            proton_image_code="i2", upload_user_id="user-001"
        )
        await memory_package_repository.save(pkg2)
        
        latest = await memory_package_repository.find_latest_by_app_id(1)
        
        assert latest is not None
        assert latest.name == "new"
    
    @pytest.mark.asyncio
    async def test_find_latest_by_app_id_no_packages(self, memory_package_repository):
        """测试查找最新包（无包）"""
        latest = await memory_package_repository.find_latest_by_app_id(999)
        
        assert latest is None

