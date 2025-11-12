import pandas as pd


def set_team_coins(team_name: str, coins: int, dir_path: str) -> None:
    """teamのcoinを設定する。

    coinの設定ファイルが存在しないときは、新規作成する。
    存在するときは、既存のファイルに追記する。
    game_idは、既存の最大値+1とする。

    ファイル名は"{team_name}_coins.csv"とする。

    Parameters
    ----------
    team_name : str
        teamの名前
    coins : int
        設定するcoinの数
    dir_path : str
        coin設定ファイルのディレクトリパス
    """
    # This is a placeholder implementation.
    df_path = f"{dir_path}/{team_name}_coins.csv"
    game_id = 0
    if df_path.exists():
        df = pd.read_csv(df_path)
        if not df.empty:
            game_id = df["game_id"].max() + 1
    df = pd.DataFrame(
        {"team_name": [team_name], "coins": [coins], "game_id": [game_id]}
    )
    df.to_csv(df_path, index=False)
