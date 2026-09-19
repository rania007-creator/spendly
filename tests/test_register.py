"""Test suite for the user registration endpoint.
"""

import re
import pytest

from app import app
from flask import url_for
from database.db import init_db, seed_db

# Ensure the tests use a fresh database and app config
@pytest.fixture
def client():
    """Create a test client with a fresh database for each test case."""
    # Reset database schema and seed demo data
    init_db()
    seed_db()
    app.config["TESTING"] = True
    with app.test_client() as client:
        # No request context is needed for setting up; just yield the client
        yield client

# Helper to extract error text from a response body

def extract_error(response):
    data = response.data.decode("utf-8")
    # The error block is rendered as <div class="auth-error">Error text</div>
    match = re.search(r"<div class=\"auth-error\">(.*?)</div>", data, re.S)
    return match.group(1).strip() if match else None

# --- Test cases -----------------------------------------------------

def test_successful_registration(client):
    response = client.post(
        "/register",
        data={
            "name": "Alice Smith",
            "email": "alice@example.com",
            "password": "Password1",
        },
        follow_redirects=False,
    )
    # Expect a redirect to the landing page
    assert response.status_code == 302
    assert response.headers["Location"] == url_for("landing")
    with client.session_transaction() as sess:
        assert "user_id" in sess
        assert sess["user_id"] is not None

# Helper to register a user within a test

def register_user(client, name, email, password):
    return client.post(
        "/register",
        data={"name": name, "email": email, "password": password},
        follow_redirects=True,
    )


def test_duplicate_email(client):
    # First registration should succeed
    register_user(client, "Bob", "bob@example.com", "Password1")
    # Second attempt with same email
    resp = register_user(client, "Charlie", "bob@example.com", "Password1")
    assert resp.status_code == 200
    assert "Email already in use." in resp.data.decode("utf-8")


def test_weak_password(client):
    resp = register_user(client, "Dave", "dave@example.com", "pass")
    assert resp.status_code == 200
    assert "Password must be at least 8 characters" in resp.data.decode("utf-8")


def test_invalid_email(client):
    resp = register_user(client, "Eve", "invalid-email", "Password1")
    assert resp.status_code == 200
    assert "Invalid email address." in resp.data.decode("utf-8")


def test_missing_field(client):
    # Missing email
    resp = register_user(client, "Frank", "", "Password1")
    assert resp.status_code == 200
    assert "Email is required." in resp.data.decode("utf-8")

# End of tests
