"""
Health Check Tests

Unit tests and integration tests for health check functionality.
"""
import pytest
from fastapi.testclient import TestClient

from src.main import create_app
from src.infrastructure.config.settings import Settings


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings."""
    return Settings(
        app_name="DIP Hub Test",
        app_version="1.0.0-test",
        debug=True,
        host="127.0.0.1",
        port=8080,
    )


@pytest.fixture
def test_client(test_settings: Settings) -> TestClient:
    """Create a test client."""
    app = create_app(test_settings)
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check_returns_healthy(self, test_client: TestClient, test_settings: Settings):
        """Test that health check returns healthy status."""
        response = test_client.get(f"{test_settings.api_prefix}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "Service is healthy"
        assert data["version"] == test_settings.app_version
    
    def test_health_check_response_format(self, test_client: TestClient, test_settings: Settings):
        """Test that health check response has correct format."""
        response = test_client.get(f"{test_settings.api_prefix}/health")
        
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert "version" in data


class TestReadyEndpoint:
    """Tests for the ready check endpoint."""
    
    def test_ready_check_returns_ready(self, test_client: TestClient, test_settings: Settings):
        """Test that ready check returns ready status."""
        response = test_client.get(f"{test_settings.api_prefix}/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "uptime_seconds" in data["checks"]
    
    def test_ready_check_response_format(self, test_client: TestClient, test_settings: Settings):
        """Test that ready check response has correct format."""
        response = test_client.get(f"{test_settings.api_prefix}/ready")
        
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert "checks" in data


class TestInfoEndpoint:
    """Tests for the service info endpoint."""
    
    def test_info_returns_service_info(self, test_client: TestClient, test_settings: Settings):
        """Test that info endpoint returns service information."""
        response = test_client.get(f"{test_settings.api_prefix}/info")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_settings.app_name
        assert data["version"] == test_settings.app_version
        assert "uptime_seconds" in data

