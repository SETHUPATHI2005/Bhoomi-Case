"""
Startup smoke tests — verify app imports cleanly and key routes respond.
Runs WITHOUT a live server (uses FastAPI TestClient / httpx).
"""
import sys
import pathlib

# Make sure `backend/` is on the path so `app.*` imports work
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=True)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_landing_page():
    r = client.get("/")
    assert r.status_code == 200


def test_login_page():
    r = client.get("/login")
    assert r.status_code == 200


def test_admin_login_page():
    """This route was previously missing from main.py — now added."""
    r = client.get("/admin-login")
    assert r.status_code == 200


def test_search_endpoint_requires_params():
    r = client.get("/api/v1/search")
    assert r.status_code == 422  # missing required query params


def test_search_returns_results():
    r = client.get("/api/v1/search", params={"village": "Kisanpur", "survey": "123"})
    assert r.status_code == 200
    data = r.json()
    assert "count" in data
    assert "results" in data


def test_admin_endpoint_requires_token():
    r = client.get("/api/v1/admin/users")
    assert r.status_code == 401


def test_admin_endpoint_rejects_bad_token():
    r = client.get("/api/v1/admin/users", headers={"X-Admin-Token": "wrong"})
    assert r.status_code == 403


def test_login_missing_fields():
    r = client.post("/api/v1/auth/login", json={})
    assert r.status_code == 400


def test_login_demo_user():
    """Demo user is seeded on startup and should be able to login."""
    r = client.post("/api/v1/auth/login", json={"username": "demo", "password": "demo123"})
    assert r.status_code == 200
    data = r.json()
    assert "token" in data
    assert data.get("user", {}).get("username") == "demo"
