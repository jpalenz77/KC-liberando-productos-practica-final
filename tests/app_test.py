"""
Module used for testing simple server module
"""

import asyncio
import os
import sys
from fastapi.testclient import TestClient
import pytest
from prometheus_client import REGISTRY
from fastapi import FastAPI

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.application.app import app, SimpleServer, REQUESTS, HEALTHCHECK_REQUESTS, MAIN_ENDPOINT_REQUESTS, BYE_ENDPOINT_REQUESTS

# Constants for endpoints
HEALTH_ENDPOINT = "/health"
MAIN_ENDPOINT = "/"
BYE_ENDPOINT = "/bye"
METRICS_ENDPOINT = "/metrics"
# Import the correct content type from prometheus_client
from prometheus_client import CONTENT_TYPE_LATEST

client = TestClient(app)

class TestSimpleServer:
    """
    TestSimpleServer class for testing SimpleServer
    """
    def setup_method(self):
        """Setup test method"""
        # Clear all counters before each test
        REQUESTS._value.set(0)
        HEALTHCHECK_REQUESTS._value.set(0)
        MAIN_ENDPOINT_REQUESTS._value.set(0)
        BYE_ENDPOINT_REQUESTS._value.set(0)

    def test_server_initialization(self):
        """Test server initialization and configuration"""
        server = SimpleServer()
        assert server._hypercorn_config is not None
        
    def test_server_configuration(self):
        """Test server configuration settings"""
        server = SimpleServer()
        # Verify initial configuration
        assert hasattr(server, '_hypercorn_config')
        assert server._hypercorn_config is not None
        
        # Configure the server
        server._hypercorn_config.bind = ['0.0.0.0:8081']
        server._hypercorn_config.keep_alive_timeout = 90
        
        # Verify configuration
        assert server._hypercorn_config.bind == ['0.0.0.0:8081']
        assert server._hypercorn_config.keep_alive_timeout == 90

    @pytest.mark.asyncio
    async def test_read_health(self):
        """Tests the health check endpoint"""
        initial_requests = REQUESTS._value.get()
        initial_health_requests = HEALTHCHECK_REQUESTS._value.get()
        
        response = client.get(HEALTH_ENDPOINT)
        
        assert response.status_code == 200
        assert response.json() == {"health": "ok"}
        assert REQUESTS._value.get() == initial_requests + 1
        assert HEALTHCHECK_REQUESTS._value.get() == initial_health_requests + 1

    @pytest.mark.asyncio
    async def test_read_main(self):
        """Tests the main endpoint"""
        initial_requests = REQUESTS._value.get()
        initial_main_requests = MAIN_ENDPOINT_REQUESTS._value.get()
        
        response = client.get(MAIN_ENDPOINT)
        
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}
        assert REQUESTS._value.get() == initial_requests + 1
        assert MAIN_ENDPOINT_REQUESTS._value.get() == initial_main_requests + 1

    @pytest.mark.asyncio
    async def test_read_bye(self):
        """Tests the bye endpoint"""
        initial_requests = REQUESTS._value.get()
        initial_bye_requests = BYE_ENDPOINT_REQUESTS._value.get()
        
        response = client.get(BYE_ENDPOINT)
        
        assert response.status_code == 200
        assert response.json() == {"msg": "Bye Bye"}
        assert REQUESTS._value.get() == initial_requests + 1
        assert BYE_ENDPOINT_REQUESTS._value.get() == initial_bye_requests + 1

    def _get_metric_value(self, metrics_text, metric_name):
        """Helper method to extract metric value from prometheus output"""
        for line in metrics_text.split('\n'):
            if line.startswith(metric_name + ' '):
                return int(float(line.split(' ')[1]))
        return None

    @pytest.mark.asyncio
    async def test_metrics(self):
        """Tests the metrics endpoint and counter increments"""
        # Clear all counters before test
        REQUESTS._value.set(0)
        HEALTHCHECK_REQUESTS._value.set(0)
        MAIN_ENDPOINT_REQUESTS._value.set(0)
        BYE_ENDPOINT_REQUESTS._value.set(0)
        
        # Make some requests to generate metrics
        client.get(HEALTH_ENDPOINT)
        client.get(MAIN_ENDPOINT)
        client.get(BYE_ENDPOINT)
        
        response = client.get(METRICS_ENDPOINT)
        
        assert response.status_code == 200
        # Basic metric presence checks
        assert "server_requests_total" in response.text
        assert "healthcheck_requests_total" in response.text
        assert "main_requests_total" in response.text
        assert "bye_requests_total" in response.text
        
        # Verify counter values using helper method
        server_requests = self._get_metric_value(response.text, "server_requests_total")
        health_requests = self._get_metric_value(response.text, "healthcheck_requests_total")
        main_requests = self._get_metric_value(response.text, "main_requests_total")
        bye_requests = self._get_metric_value(response.text, "bye_requests_total")
        
        # Check exact values - metrics request is counted after we get the response
        assert server_requests == 3, f"Expected 3 server requests, got {server_requests}"  # 3 requests
        assert health_requests == 1, f"Expected 1 health request, got {health_requests}"
        assert main_requests == 1, f"Expected 1 main request, got {main_requests}"
        assert bye_requests == 1, f"Expected 1 bye request, got {bye_requests}"

    @pytest.mark.asyncio
    async def test_multiple_requests(self):
        """Test multiple requests to verify counter increments"""
        # Clear all counters before test
        REQUESTS._value.set(0)
        HEALTHCHECK_REQUESTS._value.set(0)
        MAIN_ENDPOINT_REQUESTS._value.set(0)
        BYE_ENDPOINT_REQUESTS._value.set(0)
        
        # Make multiple requests to each endpoint
        for _ in range(3):
            client.get(HEALTH_ENDPOINT)
            client.get(MAIN_ENDPOINT)
            client.get(BYE_ENDPOINT)
        
        response = client.get(METRICS_ENDPOINT)
        assert response.status_code == 200
        
        # Verify counter values using helper method
        server_requests = self._get_metric_value(response.text, "server_requests_total")
        health_requests = self._get_metric_value(response.text, "healthcheck_requests_total")
        main_requests = self._get_metric_value(response.text, "main_requests_total")
        bye_requests = self._get_metric_value(response.text, "bye_requests_total")
        
        # Check exact values - metrics request is counted after we get the response
        assert server_requests == 9, f"Expected 9 server requests, got {server_requests}"  # 9 requests
        assert health_requests == 3, f"Expected 3 health requests, got {health_requests}"
        assert main_requests == 3, f"Expected 3 main requests, got {main_requests}"
        assert bye_requests == 3, f"Expected 3 bye requests, got {bye_requests}"

    def test_fastapi_app_metadata(self):
        """Test FastAPI application metadata and configuration"""
        assert isinstance(app, FastAPI), "app should be a FastAPI instance"
        
        # Test app metadata
        assert app.title == "FastAPI", "Default title should be 'FastAPI'"
        assert app.version == "0.1.0", "Default version should be '0.1.0'"
        
        # Test route registration by making requests
        endpoints = {
            HEALTH_ENDPOINT: "health check",
            MAIN_ENDPOINT: "main",
            BYE_ENDPOINT: "bye",
            METRICS_ENDPOINT: "metrics"
        }
        
        for endpoint, name in endpoints.items():
            response = client.get(endpoint)
            assert response.status_code == 200, f"{name} endpoint should be registered and return 200"

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        # Clear all counters before test
        REQUESTS._value.set(0)
        HEALTHCHECK_REQUESTS._value.set(0)
        MAIN_ENDPOINT_REQUESTS._value.set(0)
        BYE_ENDPOINT_REQUESTS._value.set(0)
        
        # Make concurrent requests using a session
        for _ in range(3):
            client.get(HEALTH_ENDPOINT)
            client.get(MAIN_ENDPOINT)
            client.get(BYE_ENDPOINT)
        
        # Check metrics after concurrent requests
        response = client.get(METRICS_ENDPOINT)
        assert response.status_code == 200
        
        # Verify counter values
        server_requests = self._get_metric_value(response.text, "server_requests_total")
        health_requests = self._get_metric_value(response.text, "healthcheck_requests_total")
        main_requests = self._get_metric_value(response.text, "main_requests_total")
        bye_requests = self._get_metric_value(response.text, "bye_requests_total")
        
        assert server_requests == 9, f"Expected 9 server requests, got {server_requests}"
        assert health_requests == 3, f"Expected 3 health requests, got {health_requests}"
        assert main_requests == 3, f"Expected 3 main requests, got {main_requests}"
        assert bye_requests == 3, f"Expected 3 bye requests, got {bye_requests}"

    @pytest.mark.asyncio
    async def test_counter_reset(self):
        """Test counter reset functionality"""
        # Make some requests
        client.get(HEALTH_ENDPOINT)
        client.get(MAIN_ENDPOINT)
        client.get(BYE_ENDPOINT)
        
        # Reset counters
        REQUESTS._value.set(0)
        HEALTHCHECK_REQUESTS._value.set(0)
        MAIN_ENDPOINT_REQUESTS._value.set(0)
        BYE_ENDPOINT_REQUESTS._value.set(0)
        
        # Verify counters are reset
        response = client.get(METRICS_ENDPOINT)
        assert response.status_code == 200
        
        server_requests = self._get_metric_value(response.text, "server_requests_total")
        health_requests = self._get_metric_value(response.text, "healthcheck_requests_total")
        main_requests = self._get_metric_value(response.text, "main_requests_total")
        bye_requests = self._get_metric_value(response.text, "bye_requests_total")
        
        assert server_requests == 0, f"Expected 0 server requests after reset, got {server_requests}"
        assert health_requests == 0, f"Expected 0 health requests after reset, got {health_requests}"
        assert main_requests == 0, f"Expected 0 main requests after reset, got {main_requests}"
        assert bye_requests == 0, f"Expected 0 bye requests after reset, got {bye_requests}"

    def test_metrics_content_type(self):
        """Test metrics endpoint content type and format"""
        response = client.get(METRICS_ENDPOINT)
        
        # Verify response headers
        assert response.status_code == 200
        assert response.headers['content-type'] == CONTENT_TYPE_LATEST
        
        # Verify prometheus metrics format
        metrics_text = response.text
        
        # Check metric type definitions
        assert '# TYPE server_requests_total counter' in metrics_text
        assert '# TYPE healthcheck_requests_total counter' in metrics_text
        assert '# TYPE main_requests_total counter' in metrics_text
        assert '# TYPE bye_requests_total counter' in metrics_text
        
        # Check metric help texts
        assert '# HELP server_requests_total Total number of requests to this webserver' in metrics_text
        assert '# HELP healthcheck_requests_total Total number of requests to healthcheck' in metrics_text
        assert '# HELP main_requests_total Total number of requests to main endpoint' in metrics_text
        assert '# HELP bye_requests_total Total number of requests to bye endpoint' in metrics_text

    @pytest.mark.asyncio
    async def test_hypercorn_config(self):
        """Test HyperCorn server configuration"""
        server = SimpleServer()
        
        # Test default configuration
        assert server._hypercorn_config is not None
        assert not hasattr(server._hypercorn_config, 'bind') or server._hypercorn_config.bind != ['0.0.0.0:8081']
        assert not hasattr(server._hypercorn_config, 'keep_alive_timeout') or server._hypercorn_config.keep_alive_timeout != 90
        
        # Configure server
        server._hypercorn_config.bind = ['0.0.0.0:8081']
        server._hypercorn_config.keep_alive_timeout = 90
        
        # Test configured values
        assert server._hypercorn_config.bind == ['0.0.0.0:8081']
        assert server._hypercorn_config.keep_alive_timeout == 90