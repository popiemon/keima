from pathlib import Path

import pandas as pd


def save_result(race_id: int, results: list[int], dir_path: str) -> None:
    """レース結果を保存する。

    Parameters
    ----------
    race_id : int
        レースID
    results : list[int]
        レース結果
    dir_path : str
        レース結果保存ディレクトリパス
    """
    if len(results) != 4:
        raise ValueError("results must contain exactly 4 horse numbers")

    dir_path = Path(dir_path)
    df_path = dir_path / "race_results.csv"

    # 新しい行を辞書で構築（動的に列を作成）
    new_row_dict = {"race_id": race_id}
    new_row_dict.update({f"racer_{i + 1}": results[i] for i in range(len(results))})

    if df_path.exists():
        df = pd.read_csv(df_path)
        new_row = pd.DataFrame([new_row_dict])
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = pd.DataFrame([new_row_dict])

    df.to_csv(df_path, index=False)
