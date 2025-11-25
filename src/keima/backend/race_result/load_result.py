import os
from pathlib import Path

import pandas as pd


def load_result(game_id: int, dir_path: str) -> list[int]:
    """レース結果を読み込む。

    Parameters
    ----------
    game_id : int
        レースID
    dir_path : str
        レース結果保存ディレクトリパス

    Returns
    -------
    list[int]
        レース結果
    """
    dir_path = Path(dir_path)
    df_path = dir_path / "race_results.csv"

    df = pd.read_csv(df_path)
    results = df.loc[df["game_id"] == game_id]
    if results.empty:
        raise ValueError(f"No results found for game_id {game_id}")

    KEIMA_NUM_PLAYERS = int(os.getenv("KEIMA_NUM_PLAYERS", "4"))
    result_row = results.iloc[0]
    return [result_row[f"racer_{i + 1}"] for i in range(KEIMA_NUM_PLAYERS)]
