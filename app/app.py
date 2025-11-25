from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import Depends, FastAPI, HTTPException

from keima.backend.app_class.app_class import (
    BuyTicketRequest,
    RaceState,
    RaceStateService,
    SetCoinsRequest,
)
from keima.backend.coins.get_coins import get_team_coins
from keima.backend.coins.set_coins import set_team_coins
from keima.backend.race_result.load_result import load_result
from keima.backend.race_result.save_result import save_result
from keima.backend.reward.reward import Reward

DIR_PATH = str(Path(__file__).parent.parent / "data")

app = FastAPI()

reward_cls = Reward()


race_state_service = RaceStateService()


def get_race_state_service():
    return race_state_service


@app.get("/")
def read_root():
    return {"Hello Keima"}


@app.post("/admin/set_coins")
def set_coins(req: SetCoinsRequest) -> dict:
    """各チームのcoinを設定する"""
    set_team_coins(req.team_name, req.coins, DIR_PATH, req.game_id)
    return {"team_name": req.team_name, "added_coin": req.coins}


@app.get("/get_coins")
def get_coins(team_name: str, game_id: int) -> dict:
    """各チームのcoinをgetする

    Parameters
    ----------
    team_name : str
        teamの名前
    game_id : int
        レース番号

    Returns
    -------
    dict
        team_nameとcoin数の辞書
    """
    coins = get_team_coins(team_name, DIR_PATH, game_id)
    return {"team_name": team_name, "coins": int(coins)}


@app.post("/admin/set_race_state")
def set_race_state(
    race_state: RaceState, service: RaceStateService = Depends(get_race_state_service)
) -> dict:
    """レースの状態を設定する

    Parameters
    ----------
    race_state : RaceState
        レースの状態

    Returns
    -------
    dict
        レースの状態
    """
    service.race_state = race_state
    return {"race_id": race_state.race_id, "ticket_buy": race_state.ticket_buy}


def current_race_state() -> dict:
    """内部呼び出し用: メモリ上の race_state_service から現在の状態を返す"""
    rs = race_state_service.race_state
    return {"race_id": rs.race_id, "ticket_buy": rs.ticket_buy}


@app.get("/get_race_state")
def get_race_state(service: RaceStateService = Depends(get_race_state_service)) -> dict:
    """HTTP エンドポイント: DI でサービスを受け取り現在の race_state を返す"""
    rs = service.race_state
    return {"race_id": rs.race_id, "ticket_buy": rs.ticket_buy}


@app.post("/buy_ticket")
def buy_ticket(req: BuyTicketRequest) -> dict:
    """チケットを購入する

    Parameters
    ----------
    team_name : str
        teamの名前
    request : BuyTicketRequest
        チケット情報のリスト
    Returns
    -------
    dict
        team_nameと購入したチケット数の辞書
    """
    race_state = current_race_state()
    race_id = race_state["race_id"]
    ticket_buy = race_state["ticket_buy"]
    if not ticket_buy:
        raise HTTPException(
            status_code=403, detail="Ticket purchasing is currently closed."
        )

    # チケット情報を DataFrame に変換
    ticket_df = pd.DataFrame([t.model_dump() for t in req.tickets])
    num_coins = ticket_df["unit"].sum()
    team_name = req.team_name
    team_coin = get_team_coins(team_name, DIR_PATH)
    if team_coin < num_coins:
        return {"error": "Not enough coins to purchase tickets."}

    ticket_df.to_csv(f"{DIR_PATH}/{team_name}_{race_id}_tickets.csv", index=False)
    return {"team_name": team_name, "purchased_tickets_coins": int(num_coins)}


@app.post("/admin/pay_tickets/{team_name}")
def pay_tickets(team_name: str) -> dict:
    """チームのチケットの支払いを行う
    Parameters
    ----------
    team_name : str
        teamの名前

    Returns
    -------
    dict
        team_nameと支払ったチケット数の辞書
    """
    race_state = current_race_state()
    race_id = race_state["race_id"]
    ticket_buy = race_state["ticket_buy"]
    if ticket_buy:
        return {"error": "Ticket purchasing is still open."}
    ticket_df = pd.read_csv(f"{DIR_PATH}/{team_name}_{race_id}_tickets.csv")
    # This is a placeholder implementation.
    pay_coins = ticket_df["unit"].sum()
    team_coins = get_team_coins(team_name, DIR_PATH)
    set_team_coins(team_name, team_coins - pay_coins, DIR_PATH)
    return {"team_name": team_name, "team_coins": int(team_coins - pay_coins)}


@app.post("/admin/save_race_result")
def save_race_result(result: list[int]) -> dict:
    """レースの結果を保存する

    Parameters
    ----------
    result : list[int]
        レースの結果

    Returns
    -------
    dict
        レース番号とレース結果の辞書
    """
    race_id = current_race_state()["race_id"]
    save_result(race_id, result, DIR_PATH)
    return {"race_id": race_id, "result": result}


@app.post("/admin/reward_tickets/{team_name}")
def reward_tickets(team_name: str) -> dict:
    """チームのチケットの報酬を行う
    Parameters
    ----------
    team_name : str
        teamの名前

    Returns
    -------
    dict
        team_nameと報酬したチケット数の辞書
    """
    race_state = current_race_state()
    race_id = race_state["race_id"]
    ticket_buy = race_state["ticket_buy"]
    if ticket_buy:
        return {"error": "Ticket purchasing is still open."}
    ticket_df = pd.read_csv(f"{DIR_PATH}/{team_name}_{race_id}_tickets.csv")
    result = load_result(race_id, DIR_PATH)
    reward_coins = reward_cls.reward_point(ticket_df, result)
    team_coins = get_team_coins(team_name, DIR_PATH)
    set_team_coins(team_name, team_coins + reward_coins, DIR_PATH)
    return {"team_name": team_name, "team_coins": int(team_coins + reward_coins)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
