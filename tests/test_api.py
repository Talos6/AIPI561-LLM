import pytest
import json
from fastapi.testclient import TestClient
from src.main import app
from src.cache.redis_cache import RedisCache
from unittest.mock import Mock, patch

client = TestClient(app)

@pytest.fixture
def mock_redis_cache():
    with patch('src.api.router.RedisCache') as mock:
        cache_instance = Mock()
        mock.return_value = cache_instance
        yield cache_instance

@pytest.fixture
def mock_settings():
    with patch('src.api.router.settings') as mock:
        mock.ollama_model = "tinyllama"
        mock.ollama_timeout = 30
        mock.ollama_api_url = "http://localhost:11434"
        yield mock

def test_health_check(mock_redis_cache):
    # Mock Ollama health check
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_redis_cache.ping.return_value = True
        
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "ollama": True,
            "cache": True
        }

def test_health_check_ollama_down(mock_redis_cache):
    # Mock Ollama health check failure
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")
        mock_redis_cache.ping.return_value = True
        
        response = client.get("/health")
        assert response.status_code == 503
        assert "Ollama service is not healthy" in response.json()["detail"]

def test_health_check_cache_down(mock_redis_cache):
    # Mock cache health check failure
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_redis_cache.ping.return_value = False
        
        response = client.get("/health")
        assert response.status_code == 503
        assert "Cache service is not healthy" in response.json()["detail"]

def test_generate_text_ollama(mock_redis_cache, mock_settings):
    # Mock cache miss
    mock_redis_cache.get.return_value = None
    
    # Mock Ollama health and API response
    with patch('requests.get') as mock_health:
        mock_health.return_value.status_code = 200
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {
                "response": "Generated text"
            }
            mock_post.return_value.status_code = 200
            
            response = client.post(
                "/v1/generate",
                json={
                    "prompt": "Test prompt",
                    "max_tokens": 50,
                    "temperature": 0.7
                }
            )
            
            assert response.status_code == 200
            assert response.json() == {
                "text": "Generated text",
                "model": "tinyllama",
                "cached": False
            }

def test_generate_text_cached(mock_redis_cache, mock_settings):
    # Mock cache hit
    mock_redis_cache.get.return_value = "Cached text"
    
    # Mock Ollama health check
    with patch('requests.get') as mock_health:
        mock_health.return_value.status_code = 200
        
        response = client.post(
            "/v1/generate",
            json={
                "prompt": "Test prompt",
                "max_tokens": 50,
                "temperature": 0.7
            }
        )
        
        assert response.status_code == 200
        assert response.json() == {
            "text": "Cached text",
            "model": "tinyllama",
            "cached": True
        }

def test_list_models(mock_settings):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "models": ["tinyllama", "llama2"]
        }
        mock_get.return_value.status_code = 200
        
        response = client.get("/v1/models")
        
        assert response.status_code == 200
        assert response.json() == ["tinyllama", "llama2"]

def test_list_models_no_models(mock_settings):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "models": []
        }
        mock_get.return_value.status_code = 200
        
        response = client.get("/v1/models")
        
        assert response.status_code == 200
        assert response.json() == ["tinyllama"]  # Returns default model

def test_generate_text_timeout(mock_settings):
    with patch('requests.get') as mock_health:
        mock_health.return_value.status_code = 200
        
        with patch('requests.post') as mock_post:
            mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
            
            response = client.post(
                "/v1/generate",
                json={
                    "prompt": "Test prompt"
                }
            )
            
            assert response.status_code == 504
            assert "Request to Ollama timed out" in response.json()["detail"]

def test_generate_text_error(mock_settings):
    with patch('requests.get') as mock_health:
        mock_health.return_value.status_code = 200
        
        with patch('requests.post') as mock_post:
            mock_post.side_effect = requests.exceptions.RequestException("API Error")
            
            response = client.post(
                "/v1/generate",
                json={
                    "prompt": "Test prompt"
                }
            )
            
            assert response.status_code == 500
            assert "Error generating text" in response.json()["detail"]