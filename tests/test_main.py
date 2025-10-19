"""
Test suite for FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint."""
    
    def test_read_root_success(self):
        """Test the root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Hello from FastAPI!"
        assert "environment" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"

    def test_root_endpoint_structure(self):
        """Test that root endpoint has expected structure."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = ["message", "environment", "version", "status"]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Check data types
        assert isinstance(data["message"], str)
        assert isinstance(data["environment"], str) 
        assert isinstance(data["version"], str)
        assert isinstance(data["status"], str)

    @patch.dict("os.environ", {"ENVIRONMENT": "test"}, clear=False)
    def test_root_endpoint_with_environment(self):
        """Test root endpoint respects environment variable."""
        # Need to reload modules to pick up environment changes
        from importlib import reload
        from app import config, main
        reload(config)
        reload(main)
        
        test_client = TestClient(main.app)
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["environment"] == "test"


class TestHealthEndpoint:
    """Test cases for the health endpoint."""
    
    def test_health_check_success(self):
        """Test the health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data == {"status": "healthy"}

    def test_health_check_response_format(self):
        """Test health check response format."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data
        assert isinstance(data["status"], str)


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test that invalid HTTP methods return 405."""
        response = client.post("/")
        assert response.status_code == 405


class TestCORS:
    """Test cases for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers


@pytest.fixture
def mock_environment():
    """Fixture for mocking environment variables."""
    with patch.dict("os.environ", clear=True):
        yield
