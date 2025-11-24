import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    ("game_id", "ticket_buy", "expected_response"),
    [
        (1, True, {"race_id": 1, "ticket_buy": True}),
        (2, False, {"race_id": 2, "ticket_buy": False}),
    ],
)
def test_set_race_state(
    client: TestClient,
    game_id: int,
    ticket_buy: bool,
    expected_response: dict,
) -> None:
    response = client.post(
        "/admin/set_race_state",
        json={"race_id": game_id, "ticket_buy": ticket_buy},
    )
    assert response.status_code == 200
    assert response.json() == expected_response

    response_get = client.get("/get_race_state")
    assert response_get.status_code == 200
    assert response_get.json() == expected_response