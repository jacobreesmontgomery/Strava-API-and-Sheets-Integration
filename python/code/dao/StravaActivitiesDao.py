from sqlalchemy.dialects.postgresql import insert
from models.Activity import Activity
import logging

class StravaActivitiesDao:
    """
    Responsible for managing Strava activity data in the database.
    """
    def __init__(self, db_service):
        """
        :param db_service: An instance of DatabaseService for session management.
        """
        self.db_service = db_service
        self.logger = logging.getLogger(__name__)

    def upsert_activity(self, activity_data):
        """
        Upserts an activity record into the database.
        :param activity_data: A dictionary containing activity details.
        """
        self.logger.info("Upserting activity with ID %s", activity_data.get("activity_id"))
        session = self.db_service.get_session()
        try:
            stmt = insert(Activity).values(**activity_data).on_conflict_do_update(
                index_elements=["activity_id"],  # The unique constraint column(s)
                set_={key: activity_data[key] for key in activity_data if key != "activity_id"}
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error("Error upserting activity: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def get_activity(self, activity_id):
        """
        Retrieves an activity by its ID.
        :param activity_id: The ID of the activity to retrieve.
        :return: An Activity object or None if not found.
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

    def update_activity(self, activity_id, **kwargs):
        """
        Updates fields of an activity with the specified ID.
        :param activity_id: The ID of the activity to update.
        :param kwargs: The fields and values to update.
        """
        self.logger.info("Updating activity with ID %s", activity_id)
        session = self.db_service.get_session()
        try:
            session.query(Activity).filter_by(activity_id=activity_id).update(kwargs)
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error("Error updating activity: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def delete_activity(self, activity_id):
        """
        Deletes an activity by its ID.
        :param activity_id: The ID of the activity to delete.
        """
        self.logger.info("Deleting activity with ID %s", activity_id)
        session = self.db_service.get_session()
        try:
            session.query(Activity).filter_by(activity_id=activity_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error("Error deleting activity: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()
