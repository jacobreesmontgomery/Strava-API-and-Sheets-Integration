"""
CLASS: GetAndInjectData.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will be responsible for extracting data from my
    goons through calls to the Strava API and injecting that data into 
    the "GOONS_ACTIVITIES.csv" file. 

    NOTE: Once completed, we will no longer need the DataSetup.py class
        which fetches API-extracted data from the "GOONS" sheet.
"""

# IMPORTS
from stravalib.client import Client
from stravalib.exc import RateLimitExceeded
from datetime import datetime, timedelta
from stravalib.client import Client
import csv
import os
from dotenv import load_dotenv
import json

# Loading environment variables from the .env file
load_dotenv()

# VARIABLES
ACTIVITIES_FILE_NAME = "ATHLETE_DATA"

# CLASSES
class StravaAuthorization:
    """
        Responsible for authorization of a given athlete and acquiring their newest access token.
    """
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = Client()

    def get_authorization_url(self):
        return self.client.authorization_url(client_id=self.client_id, redirect_uri=self.redirect_uri)
    
    def exchange_refresh_token(self, refresh_token):
        token_response = self.client.refresh_access_token(client_id=self.client_id, client_secret=self.client_secret, refresh_token=refresh_token)
        return token_response['access_token']

class StravaAPI:
    """
        Responsible for making calls to the Strava API for activity data.
    """
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = Client(access_token)

    def get_activities_this_week(self, athlete_id):
        try:
            # Calculate the start and end of the current week in UTC
            today = datetime.now()
            start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_week = (start_of_week + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999)
            # Retrieve activities within the current week
            activities = self.client.get_activities(after=start_of_week, before=end_of_week)
            activity_ids_and_type = [(activity.id, activity.type) for activity in activities]
            detailed_activities=list()
            for activity_id, activity_type in activity_ids_and_type:
                if activity_type == "Run": # Only including runs
                    detailed_activities.append(self.client.get_activity(activity_id=activity_id))
            return detailed_activities
        except RateLimitExceeded:
            print("Strava API rate limit exceeded. Please try again later.")
            return None
        except Exception as e:
            print(f"Failed to retrieve this week's activities for athlete {athlete_id}.")
            return None
    
    def get_activities(self, athlete_id):
        try:
            client = self.client
            activities = client.get_activities()
            return list(activities)
        except Exception as e:
            print(f"Failed to retrieve activities for athlete ID {athlete_id}: {e}")
            return None

# HELPER METHODS FOR MAIN METHOD
def get_index_of_key(dictionary, key_to_find):
    index = 0
    for key in dictionary:
        if int(key) == int(key_to_find):
            return index
        index += 1
    return -1  # Key not found in the dictionary

def format_seconds(seconds):
    """
        Formats seconds to the format of HH:MM:SS.
    """
    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format as HH:MM:SS
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def calculate_pace(total_seconds, distance_miles):
    """
        Calculates pace (MM:SS) using the total seconds and
        distance of the run (mi). 
    """
    # Convert total seconds to minutes
    total_minutes = total_seconds / 60
    
    # Calculate pace in minutes per mile
    pace_minutes_per_mile = total_minutes / distance_miles
    
    # Convert pace to MM:SS format
    pace_seconds = int(pace_minutes_per_mile * 60)
    minutes, seconds = divmod(pace_seconds, 60)
    
    return f"{minutes:02d}:{seconds:02d}"

def convert_activities_to_list(activities):
    """
        Converts the incoming activities to a list with 
        the desired columns and values.
    """
    activities_list = list()
    for activity in activities:
        activity_dict = {
            "ATHLETE": athlete_names_parallel_arr[get_index_of_key(athlete_refresh_tokens, activity.athlete.id)].upper(),
            "ACTIVITY ID": activity.id,
            "RUN": activity.name,
            "MOVING TIME": format_seconds(activity.moving_time), # Formatting to HH:MM:SS
            "DISTANCE (MI)": round(float(activity.distance) / 1609.34, 2), # Converting meters to miles
            "PACE (MIN/MI)": calculate_pace(float(activity.moving_time.total_seconds()), float(activity.distance * 0.000621371)),
            "FULL DATE": activity.start_date_local.strftime("%m/%d/%Y"),
            "TIME": activity.start_date_local.strftime("%I:%M:%S %p"),
            "DAY": activity.start_date_local.strftime("%a").upper(),
            "MONTH": activity.start_date_local.strftime("%m"),
            "DATE": activity.start_date_local.strftime("%d"),
            "YEAR": activity.start_date_local.strftime("%Y"),
            "SPM AVG": round(activity.average_cadence * 2, 2) if activity.average_cadence else "NA",
            "HR AVG": round(activity.average_heartrate, 2) if activity.average_heartrate else "NA",
            "WKT TYPE": activity.workout_type,
            "DESCRIPTION": activity.description,
            "TOTAL ELEV GAIN (FT)": round(float(str(activity.total_elevation_gain).split()[0]) * 3.28084, 2),
            "MANUAL": activity.manual,
            "MAX SPEED (FT/S)": round(float(str(activity.max_speed).split()[0]) * 3.28084, 2),
            "CALORIES": activity.calories,
            "ACHIEVEMENT COUNT": activity.achievement_count,
            "KUDOS COUNT": activity.kudos_count,
            "COMMENT COUNT": activity.comment_count,
            "ATHLETE COUNT": activity.athlete_count,
            "FULL DATETIME": activity.start_date_local.strftime("%Y-%m-%d %H:%M:%S")
            # Add more fields as needed
        }
        activities_list.append(activity_dict)
    return activities_list

def load_existing_ids(file_path, column):
    """
        Loads the existing unique IDs from the given data file.
    """
    existing_ids = set()
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for activity in reader:
            existing_ids.add(int(activity[column]))
    return existing_ids

# DRIVER
if __name__ == "__main__":
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    athlete_refresh_tokens = json.loads(os.getenv("ATHLETE_REFRESH_TOKENS"))
    athlete_names_parallel_arr = json.loads(os.getenv("ATHLETE_NAMES_PARALLEL_ARR"))

    # Initialize StravaAPI instances for each athlete
    strava_clients = {}
    for athlete_id, refresh_token in athlete_refresh_tokens.items():
        authorization_client = StravaAuthorization(client_id, client_secret, redirect_uri)
        access_token = authorization_client.exchange_refresh_token(refresh_token)
        strava_clients[athlete_id] = StravaAPI(access_token)

    athlete_count = 0
    fieldnames = [
        "ATHLETE", "ACTIVITY ID", "RUN", "MOVING TIME", 
        "DISTANCE (MI)", "PACE (MIN/MI)", "FULL DATE", "TIME", "DAY",
        "MONTH", "DATE", "YEAR", "SPM AVG",	"HR AVG",	
        "WKT TYPE", "DESCRIPTION", "TOTAL ELEV GAIN (FT)",
        "MANUAL", "MAX SPEED (FT/S)", "CALORIES", "ACHIEVEMENT COUNT",
        "KUDOS COUNT", "COMMENT COUNT", "ATHLETE COUNT",
        "FULL DATETIME"
    ]
    file_path = f"python\code\datasetup\data\{ACTIVITIES_FILE_NAME}.csv"
    unique_column = "ACTIVITY ID"
    existing_ids = load_existing_ids(file_path, unique_column)
    unique_ids = set(existing_ids)
    rows = []
    # Establishing the activities to be added to CSV file(s)
    for athlete_id, strava_client in strava_clients.items():
        activities = convert_activities_to_list(strava_client.get_activities_this_week(athlete_id))
        rows_added = 0
        if activities:
            for activity in activities:
                if activity[unique_column] not in unique_ids:
                    rows.append(activity)
                    unique_ids.add(activity[unique_column])
                    rows_added += 1
        else:
            print(f"No activities were retrieved for athlete {athlete_names_parallel_arr[athlete_count]}.")
        print(f"{rows_added} new rows were found for athlete {athlete_names_parallel_arr[athlete_count]}.")
        athlete_count += 1 # Ready for the next athlete
    
    # Sorting all new rows by the "FULL DATETIME" field
    rows.sort(key=lambda x: datetime.strptime(x['FULL DATETIME'], '%Y-%m-%d %H:%M:%S'))

    # Append sorted rows to the CSV file
    file_empty = not os.path.exists(file_path) or os.stat(file_path).st_size == 0
    with open(file_path, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
        if file_empty:
            writer.writeheader()
        writer.writerows(rows)
        print(f"{len(rows)} rows were added to {file_path}.")
