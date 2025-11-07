"""
Module used for testing simple server module
"""

from fastapi.testclient import TestClient
import pytest
import sys
from pathlib import Path

# Añadir src al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from application.app import app

client = TestClient(app)

class TestSimpleServer:
    """
    TestSimpleServer class for testing SimpleServer
    """
    @pytest.mark.asyncio
    async def test_read_health(self):
        """Tests the health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"health": "ok"}

    @pytest.mark.asyncio
    async def test_read_main(self):
        """Tests the main endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    @pytest.mark.asyncio
    async def test_read_bye(self):
        """Tests the bye endpoint"""
        response = client.get("/bye")

        assert response.status_code == 200
        assert response.json() == {"msg": "Bye Bye"}

    @pytest.mark.asyncio
    async def test_metrics(self):
        """Tests the metrics endpoint"""
        response = client.get("/metrics")

        assert response.status_code == 200
        assert "server_requests_total" in response.text
        assert "healthcheck_requests_total" in response.text
        assert "main_requests_total" in response.text
        assert "bye_requests_total" in response.text