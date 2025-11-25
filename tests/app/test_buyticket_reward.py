import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    ("team_name", "game_id", "tickets", "coins", "expected_coins"),
    [
        ("A", 1, [{"ticket_type": "win", "one": 1, "unit": 2}], 100, 98),
        (
            "B",
            1,
            [{"ticket_type": "exacta", "one": 1, "two": 2, "unit": 3}],
            100,
            97,
        ),
        (
            "C",
            1,
            [
                {"ticket_type": "trifecta", "one": 1, "two": 2, "three": 3, "unit": 1},
                {"ticket_type": "win", "one": 4, "unit": 5},
            ],
            100,
            94,
        ),
    ],
)
def test_buyticket(
    client: TestClient,
    team_name: str,
    game_id: int,
    tickets: list[dict],
    coins: int,
    expected_coins: int,
) -> None:
    # Set coins
    _ = client.post(
        "/admin/set_coins",
        json={"team_name": team_name, "coins": coins, "game_id": game_id},
    )

    # Set initial coins and allow ticket purchasing
    client.post("/admin/set_coins", json={"team_name": team_name, "coins": 1000})
    _ = client.post(
        "/admin/set_race_state",
        json={"race_id": game_id, "ticket_buy": True},
    )

    # Buy tickets
    response = client.post(
        "/buy_ticket",
        json={
            "team_name": team_name,
            "game_id": game_id,
            "tickets": tickets,
        },
    )
    assert response.status_code == 200
    purchased_coins = sum(t["unit"] for t in tickets)
    assert response.json() == {
        "team_name": team_name,
        "purchased_tickets_coins": purchased_coins,
    }

    # Close ticket purchasing
    client.post(
        "/admin/set_race_state",
        json={"race_id": game_id, "ticket_buy": False},
    )

    # # Save race result
    # client.post("/admin/save_race_result", json=result)

    # # Get reward
    # reward_response = client.post(f"/admin/reward_tickets/{team_name}")
    # assert reward_response.status_code == 200
    # # Initial coins (1000) - purchased + reward
    # assert (
    #     reward_response.json()["team_coins"] == 1000 - purchased_coins + expected_reward
    # )
