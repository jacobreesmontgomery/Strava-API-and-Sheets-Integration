from stravalib.client import Client
from stravalib.exc import RateLimitExceeded
from stravalib.model import Activity, Athlete
from datetime import datetime, timedelta
from stravalib.client import Client
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
    RetryError,
)

import os
import sys

package_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "utilities")
)
sys.path.insert(0, package_path)

from simpleLogger import simpleLogger


class StravaAuthorization:
    """
    Responsible for authorization of a given athlete and acquiring their newest access token.
    """

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = Client()

    def get_authorization_url(self) -> str:
        return self.client.authorization_url(
            client_id=self.client_id, redirect_uri=self.redirect_uri
        )

    def exchange_refresh_token(self, refresh_token: str) -> str:
        token_response = self.client.refresh_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=refresh_token,
        )
        return token_response["access_token"]

    def exchange_authorization_code(self, code):
        token_response = self.client.exchange_code_for_token(
            client_id=self.client_id, client_secret=self.client_secret, code=code
        )
        return token_response


class ActivityRetrievalException(Exception):
    """
    Exception for detailed activity retrieval failures.
    """

    pass


class StravaAPI:
    """
    Responsible for making calls to the Strava API for activity data.
    """

    def __init__(self, access_token):
        self.access_token = access_token
        self.client = Client(access_token)
        # basicConfig(
        #     level=INFO,
        #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        #     datefmt="%Y-%m-%d %H:%M:%S",
        #     filename="app.log",
        #     filemode="a"
        # )
        # self.logger = getLogger(__name__)
        self.logger = simpleLogger(log_level="INFO", class_name=__name__).logger

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(min=1, max=60),
        retry=retry_if_exception_type(ActivityRetrievalException),
    )
    def fetch_activities(
        self, start_date: str = None, end_date: str = None
    ) -> list[Activity] | None:
        """
        Retrieves all activities for the authenticated athlete.

        Returns:
            A list of activities for the authenticated athlete.
        """
        try:
            return self.client.get_activities(after=start_date, before=end_date)
        except RateLimitExceeded as e:
            self.logger.error(f"Strava API rate limit exceeded: {e}")
            return None
        except RetryError as e:
            self.logger.error(
                f"Failed to retrieve activities on final retry attempt [{e.last_attempt.attempt_number}]: {e}"
            )
            return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve activities: {e}")
            raise ActivityRetrievalException

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(min=1, max=60),
        retry=retry_if_exception_type(ActivityRetrievalException),
    )
    def fetch_detailed_activity(self, activity_id: int) -> Activity | None:
        """
        Retrieves the detailed activity with the given ID.

        Args:
            activity_id: The ID of the activity

        Returns:
            A detailed activity.
        """
        try:
            return self.client.get_activity(activity_id=activity_id)
        except RateLimitExceeded as e:
            self.logger.error(
                f"Strava API rate limit exceeded for activity [{activity_id}]: {e}"
            )
            return None
        except RetryError as e:
            self.logger.error(
                f"Failed to retrieve detailed activity [{activity_id}] on final retry attempt [{e.last_attempt.attempt_number}]: {e}"
            )
            return None
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve detailed activity with ID [{activity_id}]: {e}"
            )
            raise ActivityRetrievalException(
                f"Failed to retrieve detailed activity with ID [{activity_id}]: {e}"
            )

    def get_detailed_activities(self, activities: list[Activity]) -> list[Activity]:
        """
        Gets the detailed activities.

        Args:
            activities: list of Activity objects

        Returns:
            a list of detailed Activity objects (runs specifically)
        """
        activity_ids_and_type = [
            (activity.id, activity.type) for activity in activities
        ]
        detailed_activities: list[Activity] = []  # Type hinting and initialization
        for activity_id, activity_type in activity_ids_and_type:
            if activity_type == "Run":  # Only including runs (for now)
                detailed_activity = self.fetch_detailed_activity(
                    activity_id=activity_id
                )
                if not detailed_activity:
                    self.logger.info(
                        f"""
                        No detailed activity was acquired for activity [{activity_id}] 
                        due to a rate limit or retry error. Returning the 
                        current list of {len(detailed_activities)} detailed activities.
                    """
                    )
                    return detailed_activities  # Return what we've got (we've hit the rate limit)
                detailed_activities.append(detailed_activity)
        self.logger.info(f"Returning {len(detailed_activities)} detailed activities.")
        return detailed_activities

    def get_activities_this_week(self) -> list[Activity]:
        """
        Gets the atlete's activities for the current week.

        Returns:
            List[Activity]: A list of the current week's activities
        """
        # Calculate the start and end of the current week in UTC
        today = datetime.now()
        start_of_week = (today - timedelta(days=today.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_of_week = (start_of_week + timedelta(days=6)).replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

        # Retrieve activities within the current week
        activities = self.fetch_activities(
            start_date=start_of_week, end_date=end_of_week
        )
        if not activities:
            return []  # No activities acquired, return an empty list

        # Get the detailed activities from the basic list above
        detailed_activities = self.get_detailed_activities(activities=activities)
        return detailed_activities

    def get_activities(
        self, athlete_id: int, start_date: str = None, end_date: str = None
    ) -> list[Activity]:
        """
        Gets the athlete's activities for a default, or specified, timeframe.

        Args:
            athlete_id: The athlete's ID
            start_date: The start date, as an epoch timestamp, of the timeframe for activities (optional)
            end_date: The end date, as an epoch timestamp, of the timeframe for activities (optional)

        Returns:
            list[Activity]: A list of activities for the specified athlete and timeframe.
        """
        try:
            activities = self.fetch_activities(start_date=start_date, end_date=end_date)
            if not activities:
                return []  # No activities acquired, return an empty list
            detailed_activities = self.get_detailed_activities(activities=activities)
            return detailed_activities
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve activities for athlete ID {athlete_id}: {e}"
            )
            return None

    def get_athlete_data(self) -> Athlete:
        """
        Gets the athlete's basic information via the /athlete endpoint.

        Returns:
            An Athlete object for the given athlete.
        """
        try:
            athlete_data = self.client.get_athlete()
            return athlete_data
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving athlete data: {e}")
            return None
