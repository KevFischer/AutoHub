from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_id():
    response = client.get("/account/99999999")
    assert response.status_code == 404