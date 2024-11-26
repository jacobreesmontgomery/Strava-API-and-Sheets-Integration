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
)

# Use the Athlete model's Base
from .Athlete import Base

class Activity(Base):
    """
    Represents a single Strava run activity corresponding to the 'activities' database table.
    """
    __tablename__ = "activities"
    __table_args__ = {"schema": "strava_api"}  # To use the `strava_api` schema

    # Primary and foreign keys
    activity_id = Column(Integer, primary_key=True, autoincrement=False)
    athlete_id = Column(Integer, ForeignKey("strava_api.athletes.athlete_id"), nullable=False)

    # Athlete information
    athlete = Column(String, nullable=False)

    # Activity metadata
    run = Column(Boolean, nullable=False)
    moving_time = Column(Float, nullable=False)
    distance_mi = Column(Float, nullable=False)
    pace_min_mi = Column(Float, nullable=True)

    # Date and time fields
    full_date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    full_datetime = Column(DateTime, nullable=True)
    day = Column(String, nullable=False)
    month = Column(String, nullable=False)
    date = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # Additional activity metrics
    spm_avg = Column(Float, nullable=True)  # Steps per minute
    hr_avg = Column(Float, nullable=True)  # Heart rate average
    wkt_type = Column(String, nullable=True)  # Workout type
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
    rpe = Column(Float, nullable=True)  # Rating of Perceived Exertion
    rating = Column(Float, nullable=True)  # User-provided rating
    avg_power = Column(Float, nullable=True)  # Average power
    sleep_rating = Column(Float, nullable=True)  # Sleep quality rating

    def __repr__(self):
        return (
            f"<Activity(activity_id={self.activity_id}, athlete={self.athlete}, "
            f"distance_mi={self.distance_mi}, moving_time={self.moving_time})>"
        )
