from models.Athlete import Athlete
from sqlalchemy.orm.exc import NoResultFound
import logging

class StravaAthleteDao:
    """
    Responsible for managing athlete data in the database.
    """
    def __init__(self, db_service):
        """
        :param db_service: An instance of DatabaseService for session management.
        """
        self.db_service = db_service
        self.logger = logging.getLogger(__name__)

    def create_athlete(self, athlete_id, athlete_name, refresh_token, email):
        """
        Creates a new athlete in the database.
        :param athlete_id: The ID of the athlete.
        :param athlete_name: The name of the athlete.
        :param refresh_token: The refresh token for the athlete.
        :param email: The email of the athlete.
        :return: The athlete's ID after creation.
        """
        self.logger.info("Creating athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            athlete = Athlete(
                athlete_id=athlete_id,
                athlete_name=athlete_name,
                refresh_token=refresh_token,
                email=email
            )
            session.add(athlete)
            session.commit()
            return athlete.athlete_id
        except Exception as e:
            session.rollback()
            self.logger.error("Error creating athlete: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def get_athlete(self, athlete_id):
        """
        Retrieves an athlete by their ID.
        :param athlete_id: The ID of the athlete.
        :return: An Athlete object or None if not found.
        """
        self.logger.info("Fetching athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            return session.query(Athlete).filter_by(athlete_id=athlete_id).first()
        except NoResultFound:
            self.logger.warning("No athlete found with ID %s", athlete_id)
            return None
        except Exception as e:
            self.logger.error("Error getting athlete: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def get_athlete_id(self, athlete_name):
        """
        Retrieves an athlete's ID by their name.
        :param athlete_name: The name of the athlete.
        :return: The athlete's ID or None if not found.
        """
        self.logger.info("Fetching athlete ID for '%s'", athlete_name)
        session = self.db_service.get_session()
        try:
            athlete = session.query(Athlete).filter_by(athlete_name=athlete_name).first()
            if athlete:
                return athlete.athlete_id
            return None
        except Exception as e:
            self.logger.error("Error getting athlete ID: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def update_athlete(self, athlete_id, athlete_name=None, refresh_token=None, email=None):
        """
        Updates an athlete's details in the database.
        :param athlete_id: The ID of the athlete to update.
        :param athlete_name: The new name for the athlete.
        :param refresh_token: The new refresh token for the athlete.
        :param email: The new email for the athlete.
        """
        self.logger.info("Updating athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            athlete = session.query(Athlete).filter_by(athlete_id=athlete_id).first()
            if not athlete:
                self.logger.warning("No athlete found with ID %s", athlete_id)
                return

            if athlete_name:
                athlete.athlete_name = athlete_name
            if refresh_token:
                athlete.refresh_token = refresh_token
            if email:
                athlete.email = email

            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error("Error updating athlete: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def delete_athlete(self, athlete_id):
        """
        Deletes an athlete from the database.
        :param athlete_id: The ID of the athlete to delete.
        """
        self.logger.info("Deleting athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            athlete = session.query(Athlete).filter_by(athlete_id=athlete_id).first()
            if not athlete:
                self.logger.warning("No athlete found with ID %s", athlete_id)
                return

            session.delete(athlete)
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error("Error deleting athlete: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()
