from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_docs():
    res= client.get("/")
    assert res.status_code == 200

