import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

client = TestClient(app)


@patch('app.llm')
def test_root_endpoint(mock_llm):
    mock_llm.is_model_loaded.return_value = True
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "TINYLLAMA API is running"
    assert response.json()["model_loaded"] == True


@patch('app.llm')
def test_root_endpoint_model_not_loaded(mock_llm):
    mock_llm.is_model_loaded.return_value = False
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["model_loaded"] == False


@patch('app.llm')
def test_health_endpoint(mock_llm):
    mock_llm.is_model_loaded.return_value = True
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] == True


@patch('app.llm')
def test_health_endpoint_model_not_loaded(mock_llm):
    mock_llm.is_model_loaded.return_value = False
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] == False


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    response = client.get("/redoc")
    assert response.status_code == 200 