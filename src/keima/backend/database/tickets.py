from sqlalchemy import Column, Integer, String

from keima.backend.database.database import Base


class Tickets(Base):
    __tablename__ = "tickets"

    team_name = Column(String, primary_key=True, index=True)
    game_id = Column(Integer, index=True)
    ticket_type = Column(String, index=True)
    one = Column(Integer, index=True)
    two = Column(Integer, nullable=True, index=True)
    three = Column(Integer, nullable=True, index=True)
    unit = Column(Integer, index=True)
