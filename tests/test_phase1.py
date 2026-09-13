import requests


BASE_URL = "http://127.0.0.1:8000"


def test_home():
    response = requests.get(BASE_URL)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_gps():
    response = requests.get(
        f"{BASE_URL}/gps/2026-09-12"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["date"] == "2026-09-12"
    assert "training_load" in data


def test_recovery():
    response = requests.get(
        f"{BASE_URL}/recovery/2026-09-12"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recovery_score"] == 52


def test_wellness():
    response = requests.get(
        f"{BASE_URL}/wellness/2026-09-12"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["availability"] == "limited"


def test_matches():
    response = requests.get(
        f"{BASE_URL}/matches/2026-09-15"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["opponent"] == "Team B"
    assert data["importance"] == "high"