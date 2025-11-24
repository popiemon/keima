import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_set_race_state(client: TestClient) -> None:
    response = client.post(
        "/admin/set_race_state",
        json={"race_id": 1, "ticket_buy": True},
    )
    assert response.status_code == 200
    assert response.json() == {"race_id": 1, "ticket_buy": True}
