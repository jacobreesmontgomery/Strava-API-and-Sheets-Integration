"""
CLASS: get_and_inject_data.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will be responsible for extracting data from my
    goons through calls to the Strava API and injecting that data into 
    PostgreSQL database tables.
"""

# IMPORTS
from datetime import datetime, time
from strava_api import StravaAPI, StravaAuthorization
from stravalib.model import Activity
import os
from dotenv import load_dotenv
import json
import sys
import re

import os
import sys

package_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "utilities")
)
sys.path.insert(0, package_path)

from simple_logger import SimpleLogger

logger = SimpleLogger(log_level="INFO", class_name=__name__).logger

package_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "utilities")
)
sys.path.insert(0, package_path)

from utilities import Utilities

utilities_service = Utilities()

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(1, package_path)
from dao.strava_activities_dao import StravaActivitiesDao
from dao.services.database_service import DatabaseService

# Loading environment variables from the .env file
load_dotenv()

# VARIABLES
ACTIVITIES_FILE_NAME = "ATHLETE_DATA"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
athlete_refresh_tokens = json.loads(os.getenv("ATHLETE_REFRESH_TOKENS"))
athlete_names_parallel_arr = json.loads(os.getenv("ATHLETE_NAMES_PARALLEL_ARR"))
athlete_count = 0
ATHLETE_DATA_FIELDNAMES = json.loads(os.getenv("ATHLETE_DATA_FIELDNAMES"))
athlete_data_file = r"C:\Users\17178\Desktop\GITHUB_PROJECTS\Strava-API-and-Sheets-Integration\python\code\datasetup\data\main_data\ATHLETE_DATA.csv"
unique_column = "ACTIVITY ID"
rows = list()
RECAP_FIELDNAMES = json.loads(os.getenv("RECAP_FIELDNAMES"))
recap_filename = r"C:\Users\17178\Desktop\GITHUB_PROJECTS\Strava-API-and-Sheets-Integration\python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv"
OPTIONAL_FIELDNAMES = os.getenv("OPTIONAL_FIELDNAMES")


class DataExtractionAndInjection:

    def parse_description(self, description):
        """
        The user can optionally include RPE, rating, average power, and a sleep rating in their activity description.
        If included, we'll parse these fields out and include them in the returned dictionary.

        Example description: "RPE:3|RATING:8|POWER:135|SLEEP:8. Good run! No issues."

        Args:
            description (str): The activity description string.

        Returns:
            The parsed RPE, rating, average power, and sleep rating, if present in the description.
        """
        OPTIONAL_FIELDNAMES = ["RPE", "RATING", "POWER", "SLEEP"]
        fields = {key: 0 for key in OPTIONAL_FIELDNAMES}
        logger.debug(f"fields: {fields}")
        pattern = r"(\w+):\s*(\d+)"
        matches = re.findall(pattern, description)

        for key, value in matches:
            key = str(key).strip().upper()
            if key in OPTIONAL_FIELDNAMES:
                fields[key] = str(value).strip(". ")
                fields[key] = int(fields[key])  # Converting to int

        rpe = fields["RPE"]
        rating = fields["RATING"]
        avg_power = fields["POWER"]
        sleep_rating = fields["SLEEP"]

        logger.debug(
            f"END of parse_description() w/ return(s)... \n\trpe: {rpe}, rating: {rating}, avg_power: {avg_power}, sleep_rating: {sleep_rating}\n"
        )
        return rpe, rating, avg_power, sleep_rating

    def parse_start_date(self, start_date: datetime):
        """
        Parses the start date from a datetime object and returns it in various formats.

        Args:
            start_date: datetime object

        Returns:
            time (str): The time in HH:MM:SS format (e.g., "10:11:00")
            week_day (str): The day of the week in uppercase (e.g., "MON")
            month (int): The month number (1-12)
            day (int): The day of the month (1-31)
            year (int): The year (e.g., 2025)
        """
        week_day = start_date.strftime("%a").upper()
        month = int(start_date.strftime("%m"))
        day = int(start_date.strftime("%d"))
        year = int(start_date.strftime("%Y"))
        run_time = time(
            hour=start_date.hour,
            minute=start_date.minute,
            second=start_date.second,
            tzinfo=start_date.tzinfo,
        )

        logger.debug(
            f"\nEND of parse_start_date() w/ return(s)...\n\ttime: {time}, week_day: {week_day}, month: {month}, day: {day}, year: {year}\n"
        )
        return run_time, week_day, month, day, year

    def convert_activities_to_list_of_dicts_postgres(
        self, activities: list[Activity]
    ) -> list[dict]:
        """
        Converts the detailed activities to a list of dicts,
        digestable by SQLAlchemy for the PostgreSQL database injections.

        Args:
            activities: List of Activity objects.

        Returns:
            List[Dict] of Activity objects
        """
        logger.debug(
            f"\nSTART of convert_activities_to_list_of_dicts_postgres() w/ arg(s)...\n\tactivities: {activities}"
        )
        activities_list = list()
        for activity in activities:
            # Initial calculations
            rpe, run_rating, avg_power, sleep_rating = self.parse_description(
                activity.description if activity.description else ""
            )
            run_time, week_day, month, day, year = self.parse_start_date(
                activity.start_date_local
            )
            str_formatted_time, time_obj = utilities_service.format_seconds(
                activity.moving_time
            )
            str_formatted_moving_time, moving_time_obj = (
                utilities_service.calculate_pace(
                    float(activity.moving_time.total_seconds()),
                    float(activity.distance * 0.000621371),
                )
            )

            # Establishing the activity dict
            activity_dict = {
                "activity_id": activity.id,
                "athlete_id": activity.athlete.id,
                "name": activity.name,
                "moving_time": time_obj,
                "moving_time_s": activity.moving_time.total_seconds(),
                "distance_mi": round(
                    float(activity.distance) / 1609.34, 2
                ),  # Converting meters to miles
                "pace_min_mi": moving_time_obj,
                "avg_speed_ft_s": round(
                    float(str(activity.average_speed).split()[0]) * 3.28084, 2
                ),
                "full_datetime": activity.start_date,
                "time": run_time,
                "week_day": week_day,
                "month": month,
                "day": day,
                "year": year,
                "spm_avg": (
                    round(activity.average_cadence * 2, 2)
                    if activity.average_cadence
                    else 0.0
                ),
                "hr_avg": (
                    round(activity.average_heartrate, 2)
                    if activity.average_heartrate
                    else 0.0
                ),
                "wkt_type": activity.workout_type,
                "description": activity.description,
                "total_elev_gain_ft": round(
                    float(str(activity.total_elevation_gain).split()[0]) * 3.28084, 2
                ),
                "manual": activity.manual,
                "max_speed_ft_s": round(
                    float(str(activity.max_speed).split()[0]) * 3.28084, 2
                ),
                "calories": round(activity.calories, 0),
                "achievement_count": activity.achievement_count,
                "kudos_count": activity.kudos_count,
                "comment_count": activity.comment_count,
                "athlete_count": activity.athlete_count,
                "rpe": rpe,
                "rating": run_rating,
                "avg_power": avg_power,
                "sleep_rating": sleep_rating,
            }  # add more fields as needed
            activities_list.append(activity_dict)
        logger.debug(
            f"\nEND of convert_activities_to_list_of_dicts_postgres() w/ return(s)...\n\tactivities_list: {activities_list}\n"
        )
        return activities_list

    def get_longest_run_no_existing_data(self, new_athlete_runs):
        """
        Takes in the athlete's new data and determines the longest run
        of that data.

        NOTE: This is used in the context of their not being existing data
        for the given athlete in the recap file.
        """
        logger.debug(
            f"\nSTART of get_longest_run_no_existing_data()\n\tnew_athlete_runs: {new_athlete_runs}"
        )
        longest_run = float(new_athlete_runs[0]["DISTANCE (MI)"])
        longest_run_date = new_athlete_runs[0]["FULL DATE"]
        for new_run in new_athlete_runs[1:]:
            try:
                new_run_distance = float(new_run["DISTANCE (MI)"])
            except ValueError as e:
                logger.error(
                    f"Error: {e}"
                )  # Output: Error: could not convert string to float: 'abc'

            if new_run_distance > longest_run:
                longest_run = new_run_distance
                longest_run_date = new_run["FULL DATE"]
        logger.debug(
            f"END of get_longest_run_no_existing_data()\n\tlongest_run: {longest_run}\n\tlongest_run_date: {longest_run_date}\n"
        )
        return longest_run, longest_run_date

    def get_longest_run(self, new_athlete_runs, existing_recap_data):
        """
        Takes in the athlete's new data and determines the longest run
        of that data WITH the existing recap data.

        NOTE: This is used in the context of their being existing data
        for the given athlete in the recap file.
        """
        logger.debug(
            f"\nSTART of get_longest_run()\n\tnew_athlete_runs: {new_athlete_runs}\n\texisting_recap_data: {existing_recap_data}"
        )
        longest_run = float(existing_recap_data["LONGEST RUN"])
        longest_run_date = existing_recap_data["LONGEST RUN DATE"]
        logger.debug(
            f"longest_run: {longest_run}\nlongest_run_date: {longest_run_date}"
        )
        for new_run in new_athlete_runs[1:]:
            try:
                new_run_distance = float(new_run["DISTANCE (MI)"])
            except ValueError as e:
                logger.error(
                    f"Error: {e}"
                )  # Output: Error: could not convert string to float: 'abc'

            if new_run_distance > longest_run:
                longest_run = new_run_distance
                longest_run_date = new_run["FULL DATE"]
        logger.debug(
            f"END of get_longest_run()\n\tlongest_run: {longest_run}\n\tlongest_run_date: {longest_run_date}\n"
        )
        return longest_run, longest_run_date

    def get_and_insert_athlete_activities_into_db(
        self,
        athlete_id: int,
        refresh_token: str,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Retrieve all activities for a specific athlete from Strava API,
        format them, and insert into a MySQL database.

        Args:
            athlete_id: The athlete's ID
            refresh_token: The athlete's refresh token
            after: Limit results to activities after this timestamp
            before: Limit results to activities before this timestamp
        """
        logger.debug("\nSTART of get_and_insert_athlete_activities_into_db()...\n")

        # Get auth client and access token
        authorization_client = StravaAuthorization(
            client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
        )
        access_token = authorization_client.exchange_refresh_token(
            refresh_token=refresh_token
        )
        strava_client = StravaAPI(access_token=access_token)

        # Retrieve (and format) the athlete's activities between the after and before timeframe
        activities = strava_client.get_activities(
            athlete_id=athlete_id, start_date=start_date, end_date=end_date
        )
        if not activities:
            logger.debug(f"No activities were found for athlete {athlete_id}.")
            return  # No activities to insert
        detailed_activities = self.convert_activities_to_list_of_dicts_postgres(
            activities=activities
        )

        # Insert the formatted activities into the PostgreSQL database
        db_service = DatabaseService()
        activity_dao = StravaActivitiesDao(db_service)
        for activity in detailed_activities:
            activity_dao.upsert_activity(activity)
        logger.info(
            f"Upserted {len(detailed_activities)} activities into strava_api.activities."
        )

        logger.debug("END of get_and_insert_athlete_activities_into_db()...\n")


# Override to false for default behavior of this file
GET_AND_INSERT_TO_DB_FOR_TIMEFRAME = True
ATHLETE_INDEX = 1
START_DATE = "2025-01-01"
END_DATE = "2025-01-18"


def main():
    """
    Drives all of the main logic.
    """
    service = DataExtractionAndInjection()
    if GET_AND_INSERT_TO_DB_FOR_TIMEFRAME:
        counter = 0
        for athlete_id, refresh_token in athlete_refresh_tokens.items():
            if counter == ATHLETE_INDEX:
                service.get_and_insert_athlete_activities_into_db(
                    athlete_id=athlete_id,
                    refresh_token=refresh_token,
                    start_date=START_DATE,
                    end_date=END_DATE,
                )
                break
            counter += 1
        return


main()  # Runs every Sunday at 7:30 PM Eastern Standard Time
