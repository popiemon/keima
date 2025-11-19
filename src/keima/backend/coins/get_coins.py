import pandas as pd


def get_team_coins(team_name: str, dir_path: str, game_id: int | None = None) -> int:
    """teamのcoinを取得する。

    game_idが指定されているときは、その値に対応する行のcoinsを返す。
    指定されていないときは、dfの最後の行のcoinsを返す。

    Parameters
    ----------
    team_name : str
        teamの名前
    dir_path : str
        coin設定ファイルのディレクトリパス
    game_id : int | None, optional
        ゲームID, by default None

    Returns
    -------
    int
        dfの最後の行のcoins値
    """
    df_path = f"{dir_path}/{team_name}_coins.csv"
    df = pd.read_csv(df_path)
    if game_id is not None and len(df) > 0:
        coins = df.loc[df["game_id"] == game_id, "coins"].iloc[0]
    else:
        df = df.sort_values(by="game_id", ascending=False)
        coins = df.iloc[0]["coins"]
    return coins
