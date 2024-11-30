from sqlalchemy.dialects.postgresql import insert
from models.Activity import Activity
from DatabaseService import DatabaseService
from logging import getLogger, INFO, basicConfig

from ..utilities.simpleLogger import simpleLogger

class StravaActivitiesDao:
    """
    Responsible for managing Strava activity data in the database.
    """
    def __init__(self, db_service: DatabaseService):
        """
        :param db_service: An instance of DatabaseService for session management.
        """
        self.db_service = db_service
        # basicConfig(
        #     level=INFO,
        #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        #     datefmt="%Y-%m-%d %H:%M:%S",
        #     filename="app.log",
        #     filemode="a"
        # )
        # self.logger = getLogger(__name__)
        self.logger = simpleLogger(log_level="INFO", class_name=__name__).logger

    def upsert_activity(self, activity_data: dict) -> int:
        """
        Upserts an activity record into the database.
        
        Args:
            activity_data: A dictionary containing activity details.
        
        Returns:
            The number of rows inserted or updated in the activities table.
        """
        self.logger.info("Upserting activity with ID %s", activity_data.get("activity_id"))
        session = self.db_service.get_session()
        try:
            stmt = insert(Activity).values(**activity_data).on_conflict_do_update(
                index_elements=["activity_id"],  # The unique constraint column(s)
                set_={key: activity_data[key] for key in activity_data if key != "activity_id"}
            )
            result = session.execute(stmt)
            session.commit()
            row_count = result.rowcount
            self.logger.info(f"{row_count} rows were inserted to the activities table")
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
