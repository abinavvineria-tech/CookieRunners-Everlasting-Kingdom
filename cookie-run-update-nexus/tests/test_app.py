"""Tests for Cookie Run — Eternal Update Nexus Flask application."""

from app import create_app


def test_home_returns_200():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cookie Run" in response.data
    assert b"Eternal Update Nexus" in response.data


def test_health_returns_ok():
    app = create_app()
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_404_returns_custom_page():
    app = create_app()
    client = app.test_client()
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert b"404" in response.data


def test_home_contains_unofficial_disclaimer():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert b"Unofficial fan project" in response.data


def test_home_contains_angel_of_doom():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert b"Angel of Doom" in response.data


def test_home_contains_watchlist_cookies():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert b"White Lily Cookie" in response.data
    assert b"Pure Vanilla Cookie" in response.data
    assert b"Mogra Cookie" in response.data


def test_home_contains_ist_timezone():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert b"IST" in response.data
    assert b"UTC+5:30" in response.data


def test_home_contains_2026_archive_quarters():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert b"January" in response.data
    assert b"April" in response.data
    assert b"July" in response.data
    assert b"October" in response.data
