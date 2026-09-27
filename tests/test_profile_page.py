import pytest
from app import app
from database.db import init_db, seed_db

@pytest.fixture
def client():
    init_db()
    seed_db()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_profile_requires_login(client):
    resp = client.get("/profile")
    assert resp.status_code == 302
    from flask import url_for
    assert resp.headers["Location"].endswith(url_for("login"))


def test_profile_gets_200_authenticated(client):
    resp = client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
        follow_redirects=True,
    )
    resp = client.get("/profile")
    assert resp.status_code == 200
    data = resp.data.decode("utf-8")
    assert "Demo User" in data
    assert "demo@spendly.com" in data
    assert "DU" in data
