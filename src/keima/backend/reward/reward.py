import pandas as pd


class Reward:
    def __init__(
        self, single_rate: int = 4, quinella_rate: int = 12, trifecta_rate: int = 28
    ) -> None:
        """得点計算

        Parameters
        ----------
        single_rate : int, optional
            単勝, by default 4
        quinella_rate : int, optional
            馬連, by default 12
        trifecta_rate : int, optional
            三連単, by default 28
        """
        self.single_rate = single_rate
        self.quinella_rate = quinella_rate
        self.trifecta_rate = trifecta_rate

    def reward_point(
        self, df: pd.DataFrame, result: list[int], game_id: int | None = None
    ) -> int:
        """keimaの獲得pointを計算する

        dfのticket_typeは 'win', 'quinella', 'trifecta' のいずれかであることを想定。
        dfの予想順には、ticket_typeごとに以下のように格納されていることを想定。
        - 'win': [1頭目]
        - 'quinella': [1頭目, 2頭目]
        - 'trifecta': [1頭目, 2頭目, 3頭目]
        columnは、"game_id", "ticket_type", "unit", "one", "two", "three" を想定。
        game_idは同一ゲーム内のチケットを識別するためのID。
        game_idがNoneの場合、df内の最新のgame_idを使用する。

        Parameters
        ----------
        df : pd.DataFrame
            チケット情報のDataFrame。
        result : list[int]
            レースの結果リスト。
        game_id : int | None, optional
            ゲームID, by default None

        Returns
        -------
        int
            獲得ポイント
        """
        if len(result) != 4:
            raise ValueError("result must contain 4 horse numbers")

        if df.empty:
            return 0

        if game_id is None:
            game_id = df["game_id"].values[-1]

        df = df[df["game_id"] == game_id]

        single_tickets = df[df["ticket_type"] == "win"]
        quinella_tickets = df[df["ticket_type"] == "quinella"]
        trifecta_tickets = df[df["ticket_type"] == "trifecta"]

        point = 0

        for _, ticket in single_tickets.iterrows():
            if ticket["one"] == result[0]:
                point += self.single_rate * ticket["unit"]

        for _, ticket in quinella_tickets.iterrows():
            if ticket["one"] == result[0] and ticket["two"] == result[1]:
                point += self.quinella_rate * ticket["unit"]

        for _, ticket in trifecta_tickets.iterrows():
            if (
                ticket["one"] == result[0]
                and ticket["two"] == result[1]
                and ticket["three"] == result[2]
            ):
                point += self.trifecta_rate * ticket["unit"]

        return point
