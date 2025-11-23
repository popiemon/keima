import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_set_team_coins(client: TestClient):
    response = app.post("/set_coins/teamA", json={"coins": 100, "game_id": 1})
    assert response.status_code == 200
    assert response.json() == {"team_name": "teamA", "added_coin": 100}
