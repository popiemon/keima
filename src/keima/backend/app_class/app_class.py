from typing import Literal

from pydantic import BaseModel


class TicketInfo(BaseModel):
    """チケット情報"""

    game_id: int
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
