"""Tests for EverLink SSH Flask routes and CSRF protection."""

import os
import tempfile

import pytest

from everlink.web import create_app


@pytest.fixture
def app():
    tmp = tempfile.mkdtemp(prefix="everlink-web-test-")
    os.environ["EVERLINK_APP_DIR"] = tmp
    app = create_app()
    app.config["TESTING"] = True
    yield app
    del os.environ["EVERLINK_APP_DIR"]


@pytest.fixture
def client(app):
    return app.test_client()


def test_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"EverLink SSH" in response.data


def test_hosts_page(client):
    response = client.get("/hosts")
    assert response.status_code == 200


def test_host_add_get(client):
    response = client.get("/hosts/add")
    assert response.status_code == 200


def test_host_add_post(client):
    # First get a page to set the CSRF token in the session
    client.get("/hosts/add")
    with client.session_transaction() as sess:
        token = sess.get("csrf_token")
    response = client.post("/hosts/add", data={
        "csrf_token": token,
        "name": "web",
        "hostname": "example.com",
        "username": "alice",
        "port": "2222",
    })
    if response.status_code not in (200, 302):
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE DATA:", response.get_data(as_text=True))
    assert response.status_code in (200, 302), f"unexpected status {response.status_code}"


def test_host_add_post_missing_csrf(client):
    response = client.post("/hosts/add", data={
        "name": "web",
        "hostname": "example.com",
        "username": "alice",
        "port": "2222",
    })
    assert response.status_code == 403


def test_keys_page(client):
    response = client.get("/keys")
    assert response.status_code == 200


def test_diagnostics_page(client):
    response = client.get("/diagnostics")
    assert response.status_code == 200


def test_settings_page(client):
    response = client.get("/settings")
    assert response.status_code == 200


def test_api_hosts(client):
    response = client.get("/api/hosts")
    assert response.status_code == 200
    assert response.is_json


def test_api_connect_missing_csrf(client):
    response = client.post("/api/connect/1")
    assert response.status_code == 403
