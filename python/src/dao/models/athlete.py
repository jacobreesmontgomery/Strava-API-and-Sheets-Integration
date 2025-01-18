from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Athlete(Base):
    """
    Represents a single Strava athlete corresponding to the 'athlete' database table.
    """

    __tablename__ = "athletes"
    __table_args__ = {"schema": "strava_api"}  # Schema defined as `strava_api`

    # Primary key
    athlete_id = Column(BigInteger, primary_key=True, autoincrement=False)

    # Athlete details
    athlete_name = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return (
            f"<Athlete(athlete_id={self.athlete_id}, athlete_name={self.athlete_name}, "
            f"email={self.email})>"
        )
