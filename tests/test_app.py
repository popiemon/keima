import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ["Hello Keima"]


@pytest.mark.parametrize(
    ("team_name", "coins", "game_id", "expected_response"),
    [
        ("A", 100, 0, {"team_name": "A", "added_coin": 100}),
        ("B", 200, 1, {"team_name": "B", "added_coin": 200}),
    ],
)
def test_set_and_get_team_coins(
    client: TestClient,
    team_name: str,
    coins: int,
    game_id: int,
    expected_response: dict,
) -> None:
    response = client.post(
        "/admin/set_coins",
        json={"team_name": team_name, "coins": coins, "game_id": game_id},
    )
    assert response.status_code == 200
    assert response.json() == expected_response

    response_get = client.get(
        "/get_coins",
        params={"team_name": team_name, "game_id": game_id},
    )
    assert response_get.status_code == 200
    assert response_get.json()["team_name"] == team_name
    assert response_get.json()["coins"] == coins
