from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func
from models.activity import Activity
from python.src.dao.services.database_service import DatabaseService

import os
import sys

package_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "utilities")
)
sys.path.insert(0, package_path)

from simple_logger import SimpleLogger


class StravaActivitiesDao:
    """
    Responsible for managing Strava activity data in the database.
    """

    def __init__(self, db_service: DatabaseService):
        """
        :param db_service: An instance of DatabaseService for session management.
        """
        self.db_service = db_service
        self.logger = SimpleLogger(log_level="INFO", class_name=__name__).logger

    def upsert_activity(self, activity_data: dict) -> int:
        """
        Upserts an activity record into the database.

        Args:
            activity_data: A dictionary containing activity details.

        Returns:
            The number of rows inserted or updated in the activities table.
        """
        self.logger.debug(
            "Upserting activity with ID %s", activity_data.get("activity_id")
        )
        session = self.db_service.get_session()
        try:
            stmt = (
                insert(Activity)
                .values(**activity_data)
                .on_conflict_do_update(
                    index_elements=["activity_id"],  # The unique constraint column(s)
                    set_={
                        key: activity_data[key]
                        for key in activity_data
                        if key != "activity_id"
                    },
                )
            )
            result = session.execute(stmt)
            session.commit()
            row_count = result.rowcount
            if row_count > 0:
                self.logger.debug(f"Activity successfully upserted.")
            return row_count
        except Exception as e:
            session.rollback()
            self.logger.error("Error upserting activity: %s", e, exc_info=True)
            return 0
        finally:
            self.db_service.close_session()

    def get_activity(self, activity_id: int) -> Activity:
        """
        Retrieves an activity by its ID.

        Args:
            activity_id: The activity ID.

        Returns:
            An Activity object.
        """
        self.logger.info("Fetching activity with ID %s", activity_id)
        session = self.db_service.get_session()
        try:
            return session.query(Activity).filter_by(activity_id=activity_id).first()
        except Exception as e:
            self.logger.error("Error fetching activity: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def update_activity(self, activity_id: int, **kwargs) -> bool:
        """
        Updates fields of an activity with the specified ID.

        Args:
            activity_id: The ID of the activity to update.

        Returns:
            A boolean indicating whether or not the activity was updated.
        """
        self.logger.info("Updating activity with ID %s", activity_id)
        session = self.db_service.get_session()
        try:
            session.query(Activity).filter_by(activity_id=activity_id).update(kwargs)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            self.logger.error("Error updating activity: %s", e, exc_info=True)
            return False
        finally:
            self.db_service.close_session()

    def delete_activity(self, activity_id: int) -> bool:
        """
        Deletes an activity by its ID.

        Args:
            activity_id: The ID of the activity to delete.

        Returns:
            A boolean indicating whether the activity was deleted or not.
        """
        self.logger.info("Deleting activity with ID %s", activity_id)
        session = self.db_service.get_session()
        try:
            session.query(Activity).filter_by(activity_id=activity_id).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            self.logger.error("Error deleting activity: %s", e, exc_info=True)
            return False
        finally:
            self.db_service.close_session()

    # TODO - JACOB: Continue working on this. Think through it more and write up SQL query, then convert to SQLAlchemy query.
    def get_basic_stats(self):
        """
        Gets the basic stats, representing the current week's training, for each authenticated athlete.

        Basic stats include:
        - Tallied mileage
        - Tallied moving time
        - # of runs
        - Average mileage per run
        - Average moving time per run
        - Average pace (in minutes per mile) per run
        - Longest run
        - Date of the longest run

        Returns:
            A grouping of basic recap stats.
        """
        self.logger.info("Fetching basic stats for all authenticated athletes")
        session = self.db_service.get_session()
        try:
            # TODO: Figure out how to work with the time-based metrics
            return  # temporary return
        except Exception as e:
            self.logger.error(f"Error fetching basic stats: {e}")
            raise
