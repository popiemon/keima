from pathlib import Path

import pandas as pd


def set_team_coins(
    team_name: str, coins: int, dir_path: str, game_id: int | None = None
) -> None:
    """teamのcoinを設定する。

    coinの設定ファイルが存在しないときは、新規作成する。
    存在するときは、既存のファイルに追記する。
    game_idが指定されているときは、その値を使用する。
    game_idが指定されていないときは、既存の最大値+1とする。
    新規作成時はgame_idは0とする。

    ファイル名は"{team_name}_coins.csv"とする。

    Parameters
    ----------
    team_name : str
        teamの名前
    coins : int
        設定するcoinの数
    dir_path : str
        coin設定ファイルのディレクトリパス
    game_id : int | None, optional
        ゲームID, by default None
    """
    # This is a placeholder implementation.
    df_path = f"{dir_path}/{team_name}_coins.csv"
    if Path(df_path).exists():
        df = pd.read_csv(df_path)
        if game_id is None:
            game_id = df["game_id"].max() + 1
        new_row = pd.DataFrame(
            {"team_name": [team_name], "coins": [coins], "game_id": [game_id]}
        )
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        if game_id is None:
            game_id = 0
        df = pd.DataFrame(
            {"team_name": [team_name], "coins": [coins], "game_id": [game_id]}
        )

    df.to_csv(df_path, index=False)
