from models.Athlete import Athlete
from DatabaseService import DatabaseService
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert

import os
import sys

package_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "utilities")
)
sys.path.insert(0, package_path)

from simpleLogger import simpleLogger


class StravaAthleteDao:
    """
    Responsible for managing athlete data in the database.
    """

    def __init__(self, db_service: DatabaseService):
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

    def upsert_athlete(
        self, athlete_id: int, athlete_name: str, refresh_token: str, email: str
    ) -> int:
        """
        Inserts or updates an athlete in the database (upsert).

        Args:
            athlete_id: The athlete's ID.
            athlete_name: The name of the athlete.
            refresh_token: The refresh token for the athlete.
            email: The email of the athlete.

        Returns:
            The athlete's ID after the upsert operation.
        """
        self.logger.info("Upserting athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            stmt = (
                insert(Athlete)
                .values(
                    athlete_id=athlete_id,
                    athlete_name=athlete_name,
                    refresh_token=refresh_token,
                    email=email,
                )
                .on_conflict_do_update(
                    index_elements=[
                        "athlete_id"
                    ],  # Conflict target (e.g., primary key)
                    set_={
                        "athlete_name": athlete_name,
                        "refresh_token": refresh_token,
                        "email": email,
                    },
                )
            )
            result = session.execute(stmt)
            session.commit()
            row_count = result.rowcount
            self.logger.info(f"{row_count} rows were updated")
            return row_count
        except Exception as e:
            session.rollback()
            self.logger.error("Error upserting athlete: %s", e, exc_info=True)
            return 0
        finally:
            self.db_service.close_session()

    def get_athlete(self, athlete_id: int) -> Athlete:
        """
        Retrieves an athlete by their ID.

        Args:
            athlete_id: The athlete's ID.

        Returns:
            An Athlete object (or None if not found).
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

    def get_athlete_id(self, athlete_name: str) -> int:
        """
        Retrieves an athlete's ID by their name.

        Args:
            athlete_name: The name of the athlete.

        Returns:
            An int representing the athlete's ID (or None if not found).
        """
        self.logger.info("Fetching athlete ID for '%s'", athlete_name)
        session = self.db_service.get_session()
        try:
            athlete = (
                session.query(Athlete).filter_by(athlete_name=athlete_name).first()
            )
            if athlete:
                self.logger.info(
                    f"Acquired athlete ID of {athlete.athlete_id} for {athlete_name}"
                )
                return athlete.athlete_id
            self.logger.info("No athlete ID was found.")
            return None
        except Exception as e:
            self.logger.error("Error getting athlete ID: %s", e, exc_info=True)
            raise
        finally:
            self.db_service.close_session()

    def update_athlete(
        self,
        athlete_id: int,
        athlete_name: str = None,
        refresh_token: str = None,
        email: str = None,
    ) -> bool:
        """
        Updates an athlete's details in the database.

        Args:
            athlete_id: The athlete's ID.
            athlete_name: The new name for the athlete.
            refresh_token: The new refresh token for the athlete.
            email: The new email for the athlete.

        Returns:
            A boolean indicating whether or not the athlete's details were updated.
        """
        self.logger.info("Updating athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            athlete = session.query(Athlete).filter_by(athlete_id=athlete_id).first()
            if not athlete:
                self.logger.warning("No athlete found with ID %s", athlete_id)
                return False

            if athlete_name:
                athlete.athlete_name = athlete_name
            if refresh_token:
                athlete.refresh_token = refresh_token
            if email:
                athlete.email = email

            session.commit()
            self.logger.info("Athlete with ID %s updated", athlete_id)
            return True
        except Exception as e:
            session.rollback()
            self.logger.error("Error updating athlete: %s", e, exc_info=True)
            return False
        finally:
            self.db_service.close_session()

    def delete_athlete(self, athlete_id: int) -> bool:
        """
        Deletes an athlete from the database.

        Args:
            athlete_id: The athlete's ID.

        Returns:
            A boolean indicating whether or not the athlete was deleted.
        """
        self.logger.info("Deleting athlete with ID %s", athlete_id)
        session = self.db_service.get_session()
        try:
            athlete = session.query(Athlete).filter_by(athlete_id=athlete_id).first()
            if not athlete:
                self.logger.warning("No athlete found with ID %s", athlete_id)
                return False

            session.delete(athlete)
            session.commit()
            self.logger.info("Athlete with ID %s deleted", athlete_id)
            return True
        except Exception as e:
            session.rollback()
            self.logger.error("Error deleting athlete: %s", e, exc_info=True)
            return False
        finally:
            self.db_service.close_session()
