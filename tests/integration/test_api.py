import os
from datetime import date

import httpx
from fastapi.testclient import TestClient

from app.main import app

# Utan BASE_URL testas appen direkt i Python (TestClient).
# Med BASE_URL (t.ex. http://localhost:8000) körs samma tester mot en riktig container.
BASE_URL = os.getenv("BASE_URL")
client = httpx.Client(base_url=BASE_URL) if BASE_URL else TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_has_version_field():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_service_status_returns_forsenad_for_old_date():
    response = client.get("/service-status?type=pulver&last_service=2020-01-01")
    assert response.status_code == 200
    assert response.json()["status"] == "forsenad"


def test_service_status_returns_ok_for_service_today():
    today = date.today().isoformat()
    response = client.get(f"/service-status?type=pulver&last_service={today}")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unknown_type_gives_400():
    response = client.get("/service-status?type=glass&last_service=2026-01-01")
    assert response.status_code == 400


def test_invalid_date_gives_422():
    response = client.get("/service-status?type=pulver&last_service=inte-ett-datum")
    assert response.status_code == 422