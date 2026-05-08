import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.makedirs("logs", exist_ok=True)

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_execute_python():
    response = client.post("/api/execute", json={
        "code": "print('hello world')",
        "language": "python"
    })
    assert response.status_code == 200
    assert "hello world" in response.json().get("result", "")


def test_execute_invalid_language():
    response = client.post("/api/execute", json={
        "code": "print('hi')",
        "language": "ruby"
    })
    assert response.status_code == 422


def test_execute_empty_code():
    response = client.post("/api/execute", json={
        "code": "",
        "language": "python"
    })
    assert response.status_code == 422


def test_execute_timeout():
    response = client.post("/api/execute", json={
        "code": "while True: pass",
        "language": "python"
    })
    assert response.status_code == 200
    assert "timed out" in response.json().get("error", "").lower()


@patch("main.correct_code")
def test_ai_correct(mock_correct):
    mock_correct.return_value = "print('fixed')"
    response = client.post("/api/ai/correct", json={
        "code": "prnt('broken')",
        "language": "python"
    })
    assert response.status_code == 200
    assert "corrected_code" in response.json()


@patch("main.convert_code")
def test_ai_convert(mock_convert):
    mock_convert.return_value = ("console.log('hi')", "javascript")
    response = client.post("/api/ai/convert", json={
        "code": "print('hi')",
        "language": "python"
    })
    assert response.status_code == 200
    assert response.json()["new_language"] == "javascript"


@patch("main.explain_code")
def test_ai_explain(mock_explain):
    mock_explain.return_value = "This code prints hello."
    response = client.post("/api/ai/explain", json={
        "code": "print('hello')",
        "language": "python"
    })
    assert response.status_code == 200
    assert "explanation" in response.json()
