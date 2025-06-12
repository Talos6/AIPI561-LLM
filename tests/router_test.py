import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


@patch('src.router.llm')
def test_ask_model_not_loaded(mock_llm):
    mock_llm.is_model_loaded.return_value = False
    response = client.post("/ask", data={"prompt": "Hello"})
    assert response.status_code == 503


@patch('src.router.llm')
@patch('src.router.cache')
def test_ask_cache_hit(mock_cache, mock_llm):
    mock_llm.is_model_loaded.return_value = True
    mock_cache.get.return_value = '{"text": "cached response"}'
    response = client.post("/ask", data={"prompt": "Hello"})
    assert response.status_code == 200
    assert response.json()["cached"] == True


@patch('src.router.llm')
@patch('src.router.cache')
def test_ask_cache_miss(mock_cache, mock_llm):
    mock_llm.is_model_loaded.return_value = True
    mock_cache.get.return_value = None
    mock_llm.generate_text.return_value = "generated response"
    response = client.post("/ask", data={"prompt": "Hello"})
    assert response.status_code == 200
    assert response.json()["cached"] == False


@patch('src.router.llm')
def test_ask_generation_error(mock_llm):
    mock_llm.is_model_loaded.return_value = True
    mock_llm.generate_text.side_effect = RuntimeError("Model error")
    response = client.post("/ask", data={"prompt": "Hello"})
    assert response.status_code == 503


@patch('src.router.llm')
def test_load_model_success(mock_llm):
    mock_llm.is_model_loaded.return_value = False
    mock_llm.load_model.return_value = True
    response = client.post("/model/load")
    assert response.status_code == 200
    assert response.json()["loaded"] == True


@patch('src.router.llm')
def test_load_model_already_loaded(mock_llm):
    mock_llm.is_model_loaded.return_value = True
    response = client.post("/model/load")
    assert response.status_code == 200
    assert response.json()["loaded"] == True


@patch('src.router.llm')
def test_load_model_failure(mock_llm):
    mock_llm.is_model_loaded.return_value = False
    mock_llm.load_model.return_value = False
    response = client.post("/model/load")
    assert response.status_code == 500


@patch('src.router.llm')
def test_unload_model_success(mock_llm):
    mock_llm.unload_model.return_value = None
    response = client.post("/model/unload")
    assert response.status_code == 200
    assert response.json()["loaded"] == False


@patch('src.router.cache')
def test_clear_cache_success(mock_cache):
    mock_cache.clear.return_value = None
    response = client.delete("/cache")
    assert response.status_code == 200 