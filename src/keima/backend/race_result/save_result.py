import os
from pathlib import Path

import pandas as pd

from keima.myexception.backend import InvalidPlayerCountError


def save_result(race_id: int, result: list[int], dir_path: str) -> None:
    """レース結果を保存する。

    Parameters
    ----------
    race_id : int
        レースID
    result : list[int]
        レース結果
    dir_path : str
        レース結果保存ディレクトリパス
    """
    num_players = int(os.getenv("NUM_PLAYERS", "4"))
    if len(result) != num_players:
        raise InvalidPlayerCountError(
            f"result must contain {num_players} player numbers"
        )

    dir_path = Path(dir_path)
    df_path = dir_path / "race_result.csv"

    # 新しい行を辞書で構築（動的に列を作成）
    new_row_dict = {"race_id": race_id}
    new_row_dict.update({f"racer_{i + 1}": result[i] for i in range(len(result))})

    if df_path.exists():
        df = pd.read_csv(df_path)
        new_row = pd.DataFrame([new_row_dict])
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = pd.DataFrame([new_row_dict])

    df.to_csv(df_path, index=False)
