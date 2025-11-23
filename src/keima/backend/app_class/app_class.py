from typing import Literal

from pydantic import BaseModel


class TicketInfo(BaseModel):
    """チケット情報"""

    ticket_type: Literal["win", "exacta", "trifecta"]
    one: int
    two: int | None = None
    three: int | None = None
    unit: int = 1


class BuyTicketRequest(BaseModel):
    """チケット購入リクエスト"""

    tickets: list[TicketInfo]


class RaceState(BaseModel):
    """raceの状態を保存するクラス"""

    race_id: int = 0
    ticket_buy: bool = False


class SetCoinsRequest(BaseModel):
    """Coinの設定のクラス

    Parameters
    ----------
    team_name : str
        teamの名前
    coins : int
        設定するcoin数
    game_id : int | None, optional
        レース番号。, by default None
    """

    team_name: str
    coins: int
    game_id: int | None = None
