from fastapi.testclient import TestClient
from main import app


client = TestClient(app, raise_server_exceptions=False)
usr = "TestClientUser"
email = "Test@Client.mail"
phone = "123456789"
pw = "T3$Tcl1enT"


def test_prepare():
    """
    Delete existing datasets used by tests.
    """
    response = client.delete(url=f"account/{email}/delete")
    assert response.status_code == 200


def test_account():
    """
    Test the Account Use-Case
    by registering and logging in
    after registering.
    """
    response = client.post(url="/register/", json={
        "username": usr,
        "email": email,
        "phone": phone,
        "password": pw
    })
    assert response.status_code == 200
    response = client.post(url="/login/", json={
        "email": email,
        "password": pw
    })
    assert response.status_code == 200
