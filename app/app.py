import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

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
def set_coins(team_name: str, amount: int):
    set_team_coins(team_name, amount, DIR_PATH)
    return {"team_name": team_name, "added_coin": amount}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
