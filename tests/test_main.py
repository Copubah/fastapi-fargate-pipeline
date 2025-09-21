from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "environment" in data
    assert "version" in data
    assert data["message"] == "Hello from FastAPI!"

def test_health_check():
    """Test the health endpoint returns healthy status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "healthy"}

def test_root_endpoint_structure():
    """Test that root endpoint has expected structure"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    
    # Check all expected fields are present
    required_fields = ["message", "environment", "version"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check data types
    assert isinstance(data["message"], str)
    assert isinstance(data["environment"], str) 
    assert isinstance(data["version"], str)
