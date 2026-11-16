"""PureLily: Forever Together — Pytest test suite.

Tests cover:
- GET / → 200, home template renders with expected content
- GET /health → 200 JSON {status: ok, service: purelily-forever-together}
- GET /nonexistent → 404, custom 404 template
- Static asset references (CSS and JS) present in home HTML
- Unofficial fan-project disclaimer present on home page
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_contains_expected_content(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "PureLily" in html
    assert "The Garden Awaits" in html
    assert "Welcome Home" in html
    assert "Community Wall" in html
    assert "White Lily" in html


def test_home_has_unofficial_disclaimer(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "Unofficial fan project" in html
    assert "Devsisters" in html


def test_home_references_static_assets(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert 'static/css/style.css' in html
    assert 'static/js/main.js' in html


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "purelily-forever-together"


def test_404_returns_custom_page(client):
    response = client.get("/nonexistent-path")
    assert response.status_code == 404
    html = response.data.decode("utf-8")
    assert "404" in html
    assert "Unofficial fan project" in html
