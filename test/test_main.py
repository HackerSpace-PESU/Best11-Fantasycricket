"""
Testing for main.py
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# pylint: disable=missing-function-docstring


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_home_post():
    for i in ["a", "b", "c", "d", "e", "f"]:
        response = client.post("/", data={"match": i})
        assert response.status_code == 307


def test_result():
    response = client.post("/results")
    assert response.status_code == 200
