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
    """チケット購入リクエスト

    Parameters
    ----------
    team_name : str
        teamの名前
    game_id : int
        レース番号
    tickets : list[TicketInfo]
        購入するチケット情報のリスト
    """

    team_name: str
    game_id: int
    tickets: list[TicketInfo]


class RaceState(BaseModel):
    """raceの状態を保存するクラス

    gameの進行の仕方は、
    game_id=0, ticket_buy=False, ticket_paid=False
        ↓ 最初の状態
    game_id=0, ticket_buy=True, ticket_paid=False
        ↓ チケット購入可能状態
    game_id=0, ticket_buy=False, ticket_paid=False
        ↓ チケット購入締め切り状態
    game_id=0, ticket_buy=False, ticket_paid=True
        ↓ チケットの支払いが完了状態
    game_id=1, ticket_buy=False, ticket_paid=False
        ↓ レース結果に基づいて配当金が支払われ、次のレースへ

    Parameters
    ----------
    game_id : int
        レース番号
    ticket_buy : bool
        チケット購入可能かどうか
    ticket_paid : bool
        チケットの支払いが完了しているかどうか。Trueの場合、チケット購入はできない。
        この後、レース結果に基づいて配当金が支払われ、 ticket_paid は False にリセットされる。
    """

    game_id: int = 0
    ticket_buy: bool = False
    ticket_paid: bool = False


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


class RaceStateService:
    """レースの状態"""

    def __init__(self):
        self.race_state = RaceState()
