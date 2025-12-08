"""API 集成测试"""
import pytest
import io
import json
import zipfile
from httpx import AsyncClient, ASGITransport


@pytest.fixture
def valid_zip_bytes():
    """创建有效的ZIP字节"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        manifest = {
            "manifest_version": 1,
            "name": "Test App Package",
            "version": "1.0.0",
        }
        zf.writestr("manifest.json", json.dumps(manifest))
    return zip_buffer.getvalue()


@pytest.fixture
async def client():
    """创建测试客户端"""
    from main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthCheck:
    """健康检查测试"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """测试健康检查端点"""
        response = await client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestCreateApp:
    """创建应用API测试"""
    
    @pytest.mark.asyncio
    async def test_create_app_success(self, client):
        """测试成功创建应用"""
        response = await client.post(
            "/dip/v1/apps/",
            json={
                "name": "Test App",
                "description": "Test description",
                "dev_mode": 1,
            },
            headers={"X-User-Id": "user-001"},
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["id"] > 0
    
    @pytest.mark.asyncio
    async def test_create_app_minimal(self, client):
        """测试创建应用（最小参数）"""
        response = await client.post(
            "/dip/v1/apps/",
            json={"name": "Minimal App"},
            headers={"X-User-Id": "user-001"},
        )
        
        assert response.status_code == 201
    
    @pytest.mark.asyncio
    async def test_create_app_invalid_name(self, client):
        """测试创建应用（无效名称）"""
        response = await client.post(
            "/dip/v1/apps/",
            json={"name": ""},
            headers={"X-User-Id": "user-001"},
        )
        
        assert response.status_code == 422  # Validation error


class TestListApps:
    """应用列表API测试"""
    
    @pytest.mark.asyncio
    async def test_list_apps(self, client):
        """测试获取应用列表"""
        # 先创建一些应用
        await client.post(
            "/dip/v1/apps/",
            json={"name": "App 1"},
            headers={"X-User-Id": "user-001"},
        )
        await client.post(
            "/dip/v1/apps/",
            json={"name": "App 2"},
            headers={"X-User-Id": "user-001"},
        )
        
        response = await client.get("/dip/v1/apps/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2


class TestGetAppDetail:
    """应用详情API测试"""
    
    @pytest.mark.asyncio
    async def test_get_app_detail(self, client):
        """测试获取应用详情"""
        # 先创建应用
        create_response = await client.post(
            "/dip/v1/apps/",
            json={"name": "Detail Test App", "description": "Test desc"},
            headers={"X-User-Id": "user-001"},
        )
        app_id = create_response.json()["id"]
        
        response = await client.get(f"/dip/v1/apps/{app_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == app_id
        assert data["name"] == "Detail Test App"
        assert "app_package" in data
    
    @pytest.mark.asyncio
    async def test_get_app_detail_not_found(self, client):
        """测试获取不存在的应用详情"""
        response = await client.get("/dip/v1/apps/99999")
        
        assert response.status_code == 404


class TestUpdateApp:
    """更新应用API测试"""
    
    @pytest.mark.asyncio
    async def test_update_app(self, client):
        """测试更新应用"""
        # 先创建应用
        create_response = await client.post(
            "/dip/v1/apps/",
            json={"name": "Original Name"},
            headers={"X-User-Id": "user-001"},
        )
        app_id = create_response.json()["id"]
        
        # 更新应用
        response = await client.put(
            f"/dip/v1/apps/{app_id}",
            json={"name": "Updated Name", "description": "New desc"},
            headers={"X-User-Id": "user-002"},
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 验证更新
        detail_response = await client.get(f"/dip/v1/apps/{app_id}")
        data = detail_response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "New desc"


class TestDeleteApp:
    """删除应用API测试"""
    
    @pytest.mark.asyncio
    async def test_delete_app(self, client):
        """测试删除应用"""
        # 先创建应用
        create_response = await client.post(
            "/dip/v1/apps/",
            json={"name": "To Delete"},
            headers={"X-User-Id": "user-001"},
        )
        app_id = create_response.json()["id"]
        
        # 删除应用
        response = await client.delete(
            f"/dip/v1/apps/{app_id}",
            headers={"X-User-Id": "user-001"},
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 验证已删除
        detail_response = await client.get(f"/dip/v1/apps/{app_id}")
        assert detail_response.status_code == 404


class TestPublishUnpublish:
    """发布/撤销发布API测试"""
    
    @pytest.mark.asyncio
    async def test_publish_without_package(self, client):
        """测试发布没有包的应用"""
        # 先创建应用
        create_response = await client.post(
            "/dip/v1/apps/",
            json={"name": "No Package App"},
            headers={"X-User-Id": "user-001"},
        )
        app_id = create_response.json()["id"]
        
        # 尝试发布（应该失败）
        response = await client.post(
            f"/dip/v1/apps/{app_id}/publish",
            headers={"X-User-Id": "user-001"},
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_unpublish_not_published(self, client):
        """测试撤销未发布的应用"""
        # 先创建应用
        create_response = await client.post(
            "/dip/v1/apps/",
            json={"name": "Unpublished App"},
            headers={"X-User-Id": "user-001"},
        )
        app_id = create_response.json()["id"]
        
        # 尝试撤销（应该失败）
        response = await client.post(
            f"/dip/v1/apps/{app_id}/unpublish",
            headers={"X-User-Id": "user-001"},
        )
        
        assert response.status_code == 400

