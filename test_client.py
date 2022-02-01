from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_account_id():
    response = client.get("/account/99999999")
    assert response.status_code == 404


def test_account_posts():
    response = client.get("/unrealisticemail/posts")
    assert response.status_code == 404


def test_account_offers():
    response = client.get("/unrealisticemail/offers")
    assert response.status_code == 404


def test_account_events():
    response = client.get("/unrealisticemail/events")
    assert response.status_code == 404


def test_event_id():
    response = client.get("/event/participants/99999999")
    assert response.status_code == 404


def test_participants():
    response = client.get("/event/99999999")
    assert response.status_code == 404


def test_delete_event():
    response = client.delete("/event/99999999")
    assert response.status_code == 404


def test_forum_id():
    response = client.get("/forum/99999999")
    assert response.status_code == 404


def test_answers():
    response = client.get("/forum/answers/99999999")
    assert response.status_code == 404


def test_images():
    response = client.get("/images/99999999")
    assert response.status_code == 404


def test_offer_id():
    response = client.delete("/offer/99999999")
    assert response.status_code == 404



