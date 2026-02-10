"""健康检查 API 测试"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.asyncio
class TestHealthAPI:
    \"\"\"健康检查 API 测试类\"\"\"

    def test_health_check_endpoint(self):
        \"\"\"测试健康检查端点\"\"\"
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_check_response_structure(self):
        \"\"\"测试健康检查响应结构\"\"\"
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "app" in data
        assert "version" in data
        assert data["status"] == "ok"

    def test_api_info_endpoint(self):
        \"\"\"测试 API 信息端点\"\"\"
        response = client.get("/api/v1/info")

        assert response.status_code == 200
        assert "name" in response.json()
        assert "version" in response.json()
        assert "api_prefix" in response.json()

    def test_api_info_response_structure(self):
        \"\"\"测试 API 信息响应结构\"\"\"
        response = client.get("/api/v1/info")
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "api_prefix" in data
        assert isinstance(data["name"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["api_prefix"], str)
