import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from keima.coins.get_coins import get_team_coins
from keima.coins.set_coins import set_team_coins

DIR_PATH = "../data"

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "Keima"}


@app.post("/admin/set_coins/{team_name}")
def set_coins(team_name: str, amount: int) -> dict:
    """各チームのcoinをsetする

    Parameters
    ----------
    team_name : str
        teamの名前
    amount : int
        設定するcoinの数

    Returns
    -------
    dict
        設定したteam_nameと追加したcoin数の辞書
    """
    set_team_coins(team_name, amount, DIR_PATH)
    return {"team_name": team_name, "added_coin": amount}


@app.get("/get_coins/{team_name}")
def get_coins(team_name: str, game_id: int | None = None) -> dict:
    """各チームのcoinをgetする

    game_idが指定されていないときは、最新のcoin数を返す。
    game_idが指定されているときは、その値に対応する行のcoinsを返す。

    Parameters
    ----------
    team_name : str
        teamの名前
    game_id : int | None, optional
        レース番号。, by default None

    Returns
    -------
    dict
        team_nameとcoin数の辞書
    """
    coins = get_team_coins(team_name, DIR_PATH, game_id)
    return {"team_name": team_name, "coins": coins}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
