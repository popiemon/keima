import pandas as pd
import pytest
from keima.reward.reward import Reward

def make_df(tickets):
    """
    tickets: List[dict] with keys: game_id, ticket_type, one, two, three
    """
    return pd.DataFrame(tickets)

def test_single_win():
    df = make_df([
        {"game_id": 1, "ticket_type": "win", "one": 2, "two": None, "three": None},
        {"game_id": 1, "ticket_type": "win", "one": 3, "two": None, "three": None},
    ])
    result = [2, 1, 3, 4]
    reward = Reward(single_rate=4)
    assert reward.reward_point(df, result, 1) == 4

def test_quinella_win():
    df = make_df([
        {"game_id": 2, "ticket_type": "quinella", "one": 2, "two": 1, "three": None},
        {"game_id": 2, "ticket_type": "quinella", "one": 1, "two": 2, "three": None},
    ])
    result = [2, 1, 3, 4]
    reward = Reward(quinella_rate=12)
    assert reward.reward_point(df, result, 2) == 12

def test_trifecta_win():
    df = make_df([
        {"game_id": 3, "ticket_type": "trifecta", "one": 2, "two": 1, "three": 3},
        {"game_id": 3, "ticket_type": "trifecta", "one": 2, "two": 3, "three": 1},
    ])
    result = [2, 1, 3, 4]
    reward = Reward(trifecta_rate=28)
    assert reward.reward_point(df, result, 3) == 28

def test_multiple_tickets():
    df = make_df([
        {"game_id": 4, "ticket_type": "win", "one": 2, "two": None, "three": None},
        {"game_id": 4, "ticket_type": "win", "one": 2, "two": None, "three": None},
        {"game_id": 4, "ticket_type": "quinella", "one": 2, "two": 1, "three": None},
        {"game_id": 4, "ticket_type": "trifecta", "one": 2, "two": 1, "three": 3},
    ])
    result = [2, 1, 3, 4]
    reward = Reward()
    # 2 win tickets, 1 quinella, 1 trifecta
    assert reward.reward_point(df, result, 4) == 4*2 + 12 + 28

def test_game_id_none_uses_latest():
    df = make_df([
        {"game_id": 10, "ticket_type": "win", "one": 1, "two": None, "three": None},
        {"game_id": 11, "ticket_type": "win", "one": 2, "two": None, "three": None},
    ])
    result = [2, 1, 3, 4]
    reward = Reward()
    # Should use game_id=11
    assert reward.reward_point(df, result) == 4

def test_invalid_result_length():
    df = make_df([
        {"game_id": 1, "ticket_type": "win", "one": 2, "two": None, "three": None},
    ])
    reward = Reward()
    with pytest.raises(ValueError):
        reward.reward_point(df, [1,2,3], 1)

def test_no_tickets():
    df = make_df([])
    result = [2, 1, 3, 4]
    reward = Reward()
    assert reward.reward_point(df, result, 1) == 0
