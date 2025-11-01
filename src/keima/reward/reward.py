import pandas as pd


def reward_point(df: pd.DataFrame, result: list[int]) -> float:
    """keimaの獲得pointを計算する

    Parameters
    ----------
    df : pd.DataFrame
        チケット情報のDataFrame。
    result : list[int]
        レースの結果リスト。

    Returns
    -------
    float
        獲得ポイント
    """
    ticket_type = df["ticket_type"].values[0]
    picks = df["picks"].values[0]
    stake = df["stake"].values[0]

    if ticket_type == "win":
        if picks[0] == result[0]:
            return stake * 2.0  # 単勝は2倍
        else:
            return 0.0
    elif ticket_type == "trifecta":
        if picks == result[:3]:
            return stake * 10.0  # 三連単は10倍
        else:
            return 0.0
    else:
        return 0.0