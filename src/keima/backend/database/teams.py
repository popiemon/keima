from sqlalchemy import Column, Integer, String

from keima.backend.database.database import Base


class Coins(Base):
    __tablename__ = "coins"

    team_name = Column(String, primary_key=True, index=True)
    coins = Column(Integer, index=True)
    game_id = Column(Integer, index=True)
