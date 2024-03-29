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

# VARIABLES
DESIRED_COLUMNS=[
    "ATHLETE","ACTIVITY ID","RUN","MOVING TIME",
    "DISTANCE","PACE","FULL DATE","TIME","DAY",
    "MONTH","DATE","YEAR","SPM AVG","HR AVG",
    "WKT TYPE","DESCRIPTION"
]
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
            activity_ids = [activity.id for activity in activities]
            detailed_activities=list()
            for activity_id in activity_ids:
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
def convert_activities_to_list(activities):
    """
        Converts the incoming activities to a list with 
        the desired columns and values.
    """
    activities_list = list()
    for activity in activities:
        # This must line up with the fieldnames / headers from the CSV
        # TODO: Get all values we need, doing arithmetic as needed
        activity_dict = {
            "athlete_id": activity.athlete.id,
            "id": activity.id,
            "name": activity.name,
            "type": activity.type
            # Add more attributes as needed
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
    client_id = "83199"
    client_secret = "4d662f26d0a43fb69c2ab52e7838cc7c31736879"
    redirect_uri = "http://localhost:5000/authorization_callback"

    # Array containing athlete IDs and their corresponding refresh tokens
    athlete_refresh_tokens = {
        "37074049": "e62f800366085277ebdb8a54c81a6306f9b01fa9", # ME
        "41580846": "25a0a96e7a6f57bd393c8e76fc83c68486289790" # PATRICK LISTER
        # Add more athlete IDs and refresh tokens as needed
    }
    athlete_names_parallel_arr = [
        "Jacob Montgomery",
        "Patrick Lister"
    ]

    # Initialize StravaAPI instances for each athlete
    strava_clients = {}
    for athlete_id, refresh_token in athlete_refresh_tokens.items():
        authorization_client = StravaAuthorization(client_id, client_secret, redirect_uri)
        access_token = authorization_client.exchange_refresh_token(refresh_token)
        strava_clients[athlete_id] = StravaAPI(access_token)

    # Getting activities for each athlete
    athlete_count = 0
    fieldnames = ["athlete_id", "id", "name", "type"]
    file_path = f"python\code\datasetup\data\{ACTIVITIES_FILE_NAME}.csv"
    file_empty = not os.path.exists(file_path) or os.stat(file_path).st_size == 0
    unique_column = "id"
    existing_ids = load_existing_ids(file_path, unique_column)
    unique_ids = set(existing_ids)
    total_rows_added = 0
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
        if file_empty:
            writer.writeheader() # Write header row
        for athlete_id, strava_client in strava_clients.items():
            activities = convert_activities_to_list(strava_client.get_activities_this_week(athlete_id))
            rows_added = 0
            if activities:
                for activity in activities:
                    if activity[unique_column] not in unique_ids:
                        writer.writerow(activity)
                        unique_ids.add(activity[unique_column])
                        rows_added += 1
            else:
                print(f"No activities were retrieved for athlete {athlete_names_parallel_arr[athlete_count]}.")
            print(f"{rows_added} rows were added for athlete {athlete_names_parallel_arr[athlete_count]}.")
            athlete_count += 1 # Ready for the next athlete
            total_rows_added += rows_added
        print(f"{total_rows_added} rows were added to {file_path}.")
