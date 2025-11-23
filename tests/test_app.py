from fastapi.testclient import TestClient

from app.app import app


def test_purchase_and_result_flow():
    client = TestClient(app)

    # purchase a win ticket for user bob
    r = client.post(
        "/buy_ticket/A", json={"race_id": 1, "ticket_type": "win", "picks": [1]}
    )
    assert r.status_code == 404
    data = r.json()
    ticket_id = data["ticket_id"]

    # post results where horse 1 wins
    r = client.post("/admin/races/1/results", json={"results": [1, 2, 3, 4]})
    assert r.status_code == 200

    # get tickets for bob and assert ticket is won
    r = client.get("/users/bob/tickets")
    assert r.status_code == 200
    tickets = r.json()
    assert any(t["ticket_id"] == ticket_id and t["status"] == "won" for t in tickets)
