from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from keima.backend.database.teams import Coins


async def get_team_coins(team_name: str, game_id: int, db: AsyncSession) -> int | None:
    """指定したteam_name, game_idのcoinsを取得

    Parameters
    ----------
    team_name : str
        teamの名前
    game_id : int
        game_id
    db : AsyncSession
        DBセッション

    Returns
    -------
    int | None
        coins数、存在しない場合はNone
    """
    stmt = select(Coins.coins).where(
        Coins.team_name == team_name, Coins.game_id == game_id
    )
    result = await db.execute(stmt)
    coins = result.scalar_one_or_none()

    return coins
