"""pytest 配置和共享fixtures"""
import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock
import io
import json
import zipfile

# 将src目录添加到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domain.entities import App, AppPackage, DevMode, PublishStatus
from application.ports import IAppRepository, IAppPackageRepository, IProtonService, IPackageParser, PackageManifest, ProtonUploadResult
from application.services import AppService
from infrastructure.persistence.repositories import AppRepository, AppPackageRepository


@pytest.fixture
def mock_app_repository():
    """Mock应用仓储"""
    return AsyncMock(spec=IAppRepository)


@pytest.fixture
def mock_package_repository():
    """Mock应用包仓储"""
    return AsyncMock(spec=IAppPackageRepository)


@pytest.fixture
def mock_proton_service():
    """Mock Proton服务"""
    mock = AsyncMock(spec=IProtonService)
    mock.upload_package.return_value = ProtonUploadResult(
        chart_code="chart-abc123",
        image_code="image-def456",
    )
    return mock


@pytest.fixture
def mock_package_parser():
    """Mock包解析器"""
    mock = AsyncMock(spec=IPackageParser)
    mock.parse.return_value = PackageManifest(
        manifest_version=1,
        name="test-app",
        version="1.0.0",
    )
    mock.extract_chart.return_value = b"chart-content"
    return mock


@pytest.fixture
def app_service(mock_app_repository, mock_package_repository, mock_proton_service, mock_package_parser):
    """创建AppService实例"""
    return AppService(
        app_repository=mock_app_repository,
        package_repository=mock_package_repository,
        proton_service=mock_proton_service,
        package_parser=mock_package_parser,
    )


@pytest.fixture
def memory_app_repository():
    """内存应用仓储（用于集成测试）"""
    return AppRepository()


@pytest.fixture
def memory_package_repository():
    """内存应用包仓储（用于集成测试）"""
    return AppPackageRepository()


@pytest.fixture
def sample_app():
    """示例应用"""
    return App.create(
        name="Test App",
        creator_id="user-001",
        dev_mode=DevMode.UPLOAD,
        description="Test description",
    )


@pytest.fixture
def sample_published_app():
    """已发布的示例应用"""
    app = App.create(
        name="Published App",
        creator_id="user-001",
        dev_mode=DevMode.UPLOAD,
    )
    app.id = 1
    app.publish_status = PublishStatus.PUBLISHED
    app.release_app_package_id = 100
    return app


@pytest.fixture
def sample_package():
    """示例应用包"""
    return AppPackage.create(
        app_id=1,
        name="test-package",
        proton_chart_code="chart-123",
        proton_image_code="image-456",
        upload_user_id="user-001",
    )


@pytest.fixture
def valid_zip_file():
    """创建有效的ZIP文件"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        manifest = {
            "manifest_version": 1,
            "name": "DIP for ITOps",
            "version": "1.0.0",
        }
        zf.writestr("manifest.json", json.dumps(manifest))
        zf.writestr("client/package.tgz", b"mock-chart-content")
    
    zip_buffer.seek(0)
    return zip_buffer


@pytest.fixture
def invalid_zip_file():
    """创建无效的ZIP文件（缺少manifest.json）"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("readme.txt", "No manifest here")
    
    zip_buffer.seek(0)
    return zip_buffer

