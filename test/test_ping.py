import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_ping(client):
    response = client.get("/v1/home/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}