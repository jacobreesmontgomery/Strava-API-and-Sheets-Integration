from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
    BigInteger,
)

# Use the Athlete model's Base
from .athlete import Base


class Activity(Base):
    """
    Represents a single Strava run activity corresponding to the 'activities' database table.
    """

    __tablename__ = "activities"
    __table_args__ = {"schema": "strava_api"}  # To use the `strava_api` schema

    # Primary and foreign keys
    activity_id = Column(BigInteger, primary_key=True, autoincrement=False)
    athlete_id = Column(
        BigInteger, ForeignKey("strava_api.athletes.athlete_id"), nullable=False
    )

    # Activity metadata
    name = Column(String, nullable=False)
    moving_time = Column(Time, nullable=False)  # HH:MM:SS
    moving_time_s = Column(Integer, nullable=False)  # Moving time in seconds
    distance_mi = Column(Float, nullable=False)
    pace_min_mi = Column(Time, nullable=True)  # HH:MM:SS
    avg_speed_ft_s = Column(Float(precision=2), nullable=False)  # Average speed in ft/s

    # Date and time fields
    full_datetime = Column(DateTime, nullable=True)  # MM/DD/YY HH:MM:SS
    time = Column(Time, nullable=False)  # HH:MM:SS
    week_day = Column(String, nullable=False)  # MON-SUN
    month = Column(Integer, nullable=False)  # 1-12
    day = Column(Integer, nullable=False)  # 1-31
    year = Column(Integer, nullable=False)  # e.g. 2024

    # Additional activity metrics
    spm_avg = Column(Float, nullable=True)
    hr_avg = Column(Float, nullable=True)
    wkt_type = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    total_elev_gain_ft = Column(Float, nullable=True)
    manual = Column(Boolean, nullable=False)
    max_speed_ft_s = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)

    # Engagement metrics
    achievement_count = Column(Integer, nullable=True)
    kudos_count = Column(Integer, nullable=True)
    comment_count = Column(Integer, nullable=True)
    athlete_count = Column(Integer, nullable=True)

    # User ratings and performance
    rpe = Column(Integer, nullable=True)  # 1-10
    rating = Column(Integer, nullable=True)  # 1-10
    avg_power = Column(Integer, nullable=True)  # e.g., 305
    sleep_rating = Column(Integer, nullable=True)  # 1-10

    def __repr__(self):
        return (
            f"<Activity(activity_id={self.activity_id}, athlete={self.athlete}, "
            f"distance_mi={self.distance_mi}, moving_time={self.moving_time})>"
        )
