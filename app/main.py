from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Keima Ticket System")


class TicketCreate(BaseModel):
    race_id: int
    ticket_type: str  # 'win' or 'trifecta'
    picks: List[int]
    stake: Optional[int] = 1


class TicketOut(BaseModel):
    ticket_id: int
    race_id: int
    ticket_type: str
    picks: List[int]
    status: str  # pending, won, lost


class RaceResult(BaseModel):
    results: List[int]


# In-memory stores for demo purposes
users = {
    # example user
    "alice": {"username": "alice", "coin": 10, "balance": 0},
}

races = {
    1: {
        "race_id": 1,
        "race_name": "第1レース",
        "horses": [1, 2, 3, 4],
        "results": None,
        # pools track total stakes by ticket_type
        "pools": {"win": 0, "trifecta": 0},
        # detailed stakes per pick: 'win' -> {horse: total_stakes}, 'trifecta' -> {(a,b,c): total_stakes}
        "stakes": {"win": {}, "trifecta": {}},
    }
}

tickets = {}
_ticket_seq = 100


def _next_ticket_id() -> int:
    global _ticket_seq
    _ticket_seq += 1
    return _ticket_seq


def _validate_ticket_create(tc: TicketCreate):
    if tc.race_id not in races:
        raise HTTPException(status_code=404, detail="race not found")
    if tc.ticket_type not in ("win", "trifecta"):
        raise HTTPException(status_code=400, detail="invalid ticket_type")
    if tc.ticket_type == "win" and len(tc.picks) != 1:
        raise HTTPException(status_code=400, detail="win requires exactly 1 pick")
    if tc.ticket_type == "trifecta" and len(tc.picks) != 3:
        raise HTTPException(status_code=400, detail="trifecta requires exactly 3 picks")
    # check picks are within horses
    for p in tc.picks:
        if p not in races[tc.race_id]["horses"]:
            raise HTTPException(status_code=400, detail=f"invalid pick: {p}")
    if tc.stake is None or tc.stake <= 0:
        raise HTTPException(status_code=400, detail="stake must be positive integer")


@app.post("/users/{username}/tickets")
def purchase_ticket(username: str, body: TicketCreate):
    # ensure user exists
    user = users.get(username)
    if user is None:
        # create user with default coins
        users[username] = {"username": username, "coin": 10, "balance": 0}
        user = users[username]

    # validate request
    _validate_ticket_create(body)

    stake = body.stake or 1
    # require stake coins per ticket
    if user["coin"] < stake:
        raise HTTPException(status_code=400, detail="not enough coins")

    user["coin"] -= stake
    tid = _next_ticket_id()
    tickets[tid] = {
        "ticket_id": tid,
        "user": username,
        "race_id": body.race_id,
        "ticket_type": body.ticket_type,
        "picks": body.picks,
        "stake": stake,
        "status": "pending",
    }

    # update race pools and stakes breakdown
    race = races[body.race_id]
    race["pools"][body.ticket_type] += stake
    if body.ticket_type == "win":
        horse = body.picks[0]
        race["stakes"]["win"][horse] = race["stakes"]["win"].get(horse, 0) + stake
    else:
        key = tuple(body.picks)
        race["stakes"]["trifecta"][key] = race["stakes"]["trifecta"].get(key, 0) + stake

    return {"message": "Ticket purchased successfully.", "ticket_id": tid, "remaining_coins": user["coin"]}


@app.get("/users/{username}/tickets", response_model=List[TicketOut])
def list_tickets(username: str):
    user = users.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    res = []
    for t in tickets.values():
        if t["user"] == username:
            res.append({
                "ticket_id": t["ticket_id"],
                "race_id": t["race_id"],
                "ticket_type": t["ticket_type"],
                "picks": t["picks"],
                "status": t["status"],
            })
    return res


@app.post("/admin/races/{race_id}/results")
def post_results(race_id: int, body: RaceResult):
    if race_id not in races:
        raise HTTPException(status_code=404, detail="race not found")
    if len(body.results) != 4:
        raise HTTPException(status_code=400, detail="results must contain 4 horse numbers")

    races[race_id]["results"] = body.results

    # Evaluate tickets for this race using pari-mutuel style payout
    # take_rate: operator's cut from the pool
    take_rate = 0.15

    race = races[race_id]
    pool_win = race["pools"].get("win", 0)
    pool_trif = race["pools"].get("trifecta", 0)
    win_horse = body.results[0]
    trifecta_key = tuple(body.results[0:3])

    # compute total stakes on winning picks
    stakes_on_win = race["stakes"]["win"].get(win_horse, 0)
    stakes_on_trif = race["stakes"]["trifecta"].get(trifecta_key, 0)

    # For each ticket in the race, determine status and payout
    for t in tickets.values():
        if t["race_id"] != race_id:
            continue
        if t["ticket_type"] == "win":
            if t["picks"][0] == win_horse:
                t["status"] = "won"
                # If there are stakes on the winning horse, distribute proportional share of pool
                if stakes_on_win > 0:
                    # payout includes stake; proportional share = (ticket_stake / stakes_on_win) * (pool_win * (1 - take_rate))
                    payout = int((t["stake"] / stakes_on_win) * (pool_win * (1 - take_rate)))
                else:
                    payout = 0
                users[t["user"]]["coin"] += payout
                users[t["user"]]["balance"] += payout
            else:
                t["status"] = "lost"
        elif t["ticket_type"] == "trifecta":
            if tuple(t["picks"]) == trifecta_key:
                t["status"] = "won"
                if stakes_on_trif > 0:
                    payout = int((t["stake"] / stakes_on_trif) * (pool_trif * (1 - take_rate)))
                else:
                    payout = 0
                users[t["user"]]["coin"] += payout
                users[t["user"]]["balance"] += payout
            else:
                t["status"] = "lost"

    return {"message": f"Race results for race_id {race_id} have been recorded."}


@app.get("/races/{race_id}")
def get_race(race_id: int):
    if race_id not in races:
        raise HTTPException(status_code=404, detail="race not found")
    r = races[race_id]
    return {"race_id": r["race_id"], "race_name": r["race_name"], "horses": r["horses"], "results": r["results"]}
