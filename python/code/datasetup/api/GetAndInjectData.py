"""
CLASS: GetAndInjectData.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will be responsible for extracting data from my
    goons through calls to the Strava API and injecting that data into 
    the "ATHLETE_DATA.csv" file. 

    NOTE: Once completed, we will no longer need the DataSetup.py class
        which fetches API-extracted data from the "GOONS" sheet.
"""

# IMPORTS
from datetime import datetime
from StravaAPI import StravaAPI, StravaAuthorization
import csv
import os
from dotenv import load_dotenv
import json
import emoji
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utilities'))
sys.path.insert(0, package_path)

from utilities import (
    get_index_of_key,
    format_seconds,
    calculate_pace,
    divide_time_str_by_number,
    tally_time
)

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
athlete_data_file = f"python\code\datasetup\data\main_data\{ACTIVITIES_FILE_NAME}.csv"
unique_column = "ACTIVITY ID"
rows = list()
RECAP_FIELDNAMES = json.loads(os.getenv("RECAP_FIELDNAMES"))
recap_filename = r'python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv'
OPTIONAL_FIELDNAMES = os.getenv("OPTIONAL_FIELDNAMES")

# TODO: Update recap data to include the averages for the newly added optional fieldnames


# HELPER METHODS FOR MAIN METHOD
# TODO: Test this out. Get test class working.
def parse_description(description):
    """
        The user can optionally include RPE, rating, average power, and a sleep rating in their activity description.
        If included, we'll parse these fields out and include them in the returned dictionary.

        Example description: "RPE:3|RATING:8|POWER:135|SLEEP:8. Good run! No issues."

        Args:
            description (str): The activity description string.
        
        Returns:
            The parsed RPE, rating, average power, and sleep rating, if present in the description.
    """
    print(f"\nSTART of parse_description() w/ arg(s)...\n\tdescription: {description}")
    rpe = rating = avgPower = sleepRating = "N/A" # Default to "N/A" if these aren't found in the description
    descArr = description.split(".")
    fieldsArr = descArr[0].split("|")
    for i in range(len(fieldsArr)):
        fieldArr = fieldsArr[i].split(":")
        if len(fieldArr) != 2 or len(fieldArr) == 0:
            print(f"Error: Invalid field format in description. Expected 'FIELD:VALUE'.")
            continue
        elif not fieldArr or fieldArr == None:
            print(f"Error: Empty field in description.")
            continue
        # Process the field name
        fieldArr[0] = str(fieldArr[0]).strip().upper()
        if fieldArr[0] not in OPTIONAL_FIELDNAMES:
            print(f"Error: Field [{fieldArr[0]}] is not accepted for data ingestion at this time.")
            continue
        # Process the value
        fieldArr[1] = str(fieldArr[1]).strip()
        try:
            fieldArr[1] = int(fieldArr[1])
        except ValueError:
            print(f"Error: Could not convert value [{fieldArr[1]}] to an integer.")
            continue
        # Assign the value to the appropriate field
        if (fieldArr[0] == "RPE"):
            rpe = fieldArr[1] if fieldArr[1] else "N/A"
        elif (fieldArr[0] == "RATING"):
            rating = fieldArr[1] if fieldArr[1] else "N/A"
        elif (fieldArr[0] == "POWER"):
            avgPower = fieldArr[1] if fieldArr[1] else "N/A"
        elif (fieldArr[0] == "SLEEP"):
            sleepRating = fieldArr[1] if fieldArr[1] else "N/A"
    print(f"END of parse_description() w/ return(s)... \n\trpe: {rpe}, rating: {rating}, avgPower: {avgPower}, sleepRating: {sleepRating}\n")
    return rpe, rating, avgPower, sleepRating

def convert_activities_to_list_of_dicts(activities):
    """
        Converts the incoming activities to a list with 
        the desired columns and values.
    """
    print(f"\nSTART of convert_activities_to_list_of_dicts() w/ arg(s)...\n\tactivities: {activities}")
    activities_list = list()
    for activity in activities:
        rpe, runRating, avgPower, sleepRating = parse_description(activity.description if activity.description else "")
        activity_dict = {
            "ATHLETE": athlete_names_parallel_arr[get_index_of_key(athlete_refresh_tokens, activity.athlete.id)].upper(),
            "ACTIVITY ID": activity.id,
            "RUN": activity.name,
            "MOVING TIME": format_seconds(activity.moving_time), # Formatting to HH:MM:SS
            "DISTANCE (MI)": f"{round(float(activity.distance) / 1609.34, 2):.2f}", # Converting meters to miles
            "PACE (MIN/MI)": calculate_pace(float(activity.moving_time.total_seconds()), float(activity.distance * 0.000621371)),
            "FULL DATE": activity.start_date_local.strftime("%m/%d/%Y"),
            "TIME": activity.start_date_local.strftime("%I:%M:%S %p"),
            "DAY": activity.start_date_local.strftime("%a").upper(),
            "MONTH": activity.start_date_local.strftime("%m"),
            "DATE": activity.start_date_local.strftime("%d"),
            "YEAR": activity.start_date_local.strftime("%Y"),
            "SPM AVG": f"{round(activity.average_cadence * 2, 2):.2f}" if activity.average_cadence else "NA",
            "HR AVG": f"{round(activity.average_heartrate, 2):.2f}" if activity.average_heartrate else "NA",
            "WKT TYPE": activity.workout_type,
            "DESCRIPTION": activity.description,
            "TOTAL ELEV GAIN (FT)": f"{round(float(str(activity.total_elevation_gain).split()[0]) * 3.28084, 2):.2f}",
            "MANUAL": activity.manual,
            "MAX SPEED (FT/S)": f"{round(float(str(activity.max_speed).split()[0]) * 3.28084, 2):.2f}",
            "CALORIES": round(activity.calories, 0),
            "ACHIEVEMENT COUNT": activity.achievement_count,
            "KUDOS COUNT": activity.kudos_count,
            "COMMENT COUNT": activity.comment_count,
            "ATHLETE COUNT": activity.athlete_count,
            "FULL DATETIME": activity.start_date_local.strftime("%Y-%m-%d %H:%M:%S"),
            "RPE": rpe,
            "RATING": runRating,
            "AVG POWER": avgPower,
            "SLEEP RATING": sleepRating
            # Add more fields as needed
        }
        activities_list.append(activity_dict)
    print(f"\nEND of convert_activities_to_list_of_dicts() w/ return(s)...\n\tactivities_list: {activities_list}\n")
    return activities_list


def load_existing_ids(file_path, column):
    """
        Loads the existing unique IDs from the given data file.
    """
    print(f"\nSTART of load_existing_ids() w/ arg(s)...\n\tfile_path: {file_path}\n\tcolumn: {column}\n")
    existing_ids = set()
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for activity in reader:
            existing_ids.add(int(activity[column]))
    print(f"\nEND of load_existing_ids() w/ return(s)...\n\texisting_ids: {existing_ids}\n")
    return existing_ids


def get_longest_run_no_existing_data(new_athlete_runs):
    """
        Takes in the athlete's new data and determines the longest run
        of that data.

        NOTE: This is used in the context of their not being existing data
        for the given athlete in the recap file.
    """
    print(f"\nSTART of get_longest_run_no_existing_data()\n\tnew_athlete_runs: {new_athlete_runs}")
    longest_run = float(new_athlete_runs[0]["DISTANCE (MI)"])
    longest_run_date = new_athlete_runs[0]["FULL DATE"]
    for new_run in new_athlete_runs[1:]:
        try:
            new_run_distance = float(new_run["DISTANCE (MI)"])
        except ValueError as e:
            print(f"Error: {e}")  # Output: Error: could not convert string to float: 'abc'

        if new_run_distance > longest_run:
            longest_run = new_run_distance
            longest_run_date = new_run["FULL DATE"]
    print(f"END of get_longest_run_no_existing_data()\n\tlongest_run: {longest_run}\n\tlongest_run_date: {longest_run_date}\n")
    return longest_run, longest_run_date


def get_longest_run(new_athlete_runs, existing_recap_data):
    """
        Takes in the athlete's new data and determines the longest run
        of that data WITH the existing recap data.

        NOTE: This is used in the context of their being existing data
        for the given athlete in the recap file.
    """
    print(f"\nSTART of get_longest_run()\n\tnew_athlete_runs: {new_athlete_runs}\n\texisting_recap_data: {existing_recap_data}")
    longest_run = float(existing_recap_data["LONGEST RUN"])
    longest_run_date = existing_recap_data["LONGEST RUN DATE"]
    print(f"longest_run: {longest_run}\nlongest_run_date: {longest_run_date}")
    for new_run in new_athlete_runs[1:]:
        try:
            new_run_distance = float(new_run["DISTANCE (MI)"])
        except ValueError as e:
            print(f"Error: {e}")  # Output: Error: could not convert string to float: 'abc'
        
        if new_run_distance > longest_run:
            longest_run = new_run_distance
            longest_run_date = new_run["FULL DATE"]
    print(f"END of get_longest_run()\n\tlongest_run: {longest_run}\n\tlongest_run_date: {longest_run_date}\n")
    return longest_run, longest_run_date


def query_new_runs(rows, athlete_name):
    """
        Queries for new runs for the given athlete.
    """
    print(f"\nSTART of query_new_runs() w/ arg(s)...\n\trows: {rows}\n\tathlete_name: {athlete_name}")
    new_athlete_runs = [activity for activity in rows if str(activity["ATHLETE"].upper()) == athlete_name.upper()]
    print(f"END of query_new_runs() w/ return(s)...\n\tnew_athlete_runs: {new_athlete_runs}\n")
    return new_athlete_runs


def write_athlete_data(new_athlete_runs, athlete_name):
    """
        Writes the incoming runs to the athlete's weekly stats file.
    """
    print(f"\nSTART of write_athlete_data() w/ arg(s)...\n\tnew_athlete_runs: {new_athlete_runs}")
    athlete_week_file = f"python\code\datasetup\data\weekly_stats\{athlete_name.upper()}_WEEK_STATS.csv"
    with open(athlete_week_file, 'a+', newline='') as athlete_stat_file:
        writer = csv.DictWriter(athlete_stat_file, fieldnames=ATHLETE_DATA_FIELDNAMES, delimiter=',')
        if not os.path.exists(athlete_week_file) or os.stat(athlete_week_file).st_size == 0:
            writer.writeheader()
        writer.writerows(new_athlete_runs) # Writing the new runs to the athlete's CSV file
        print(f"Added {len(new_athlete_runs)} rows to CSV file {athlete_week_file}.")
    print(f"END of write_athlete_data()\n")


def query_existing_recap_data(athlete_name):
    """
        Queries for existing recap data.
    """
    print(f"\nSTART of query_existing_recap_data() w/ arg(s)...\n\tathlete_name: {athlete_name}")
    existing_recap_data = dict()
    with open(recap_filename, 'r+', newline='') as recap_file: 
        # Writing headers if they don't exist
        writer = csv.DictWriter(recap_file, fieldnames=RECAP_FIELDNAMES, delimiter=',')
        if not os.path.exists(recap_filename) or os.stat(recap_filename).st_size == 0:
            writer.writeheader()
            recap_file.seek(0)  # Move the file pointer back to the start of the file
        reader = csv.DictReader(recap_file, fieldnames=RECAP_FIELDNAMES, delimiter=',')
        
        try:
            next(reader)  # Skipping header
        except StopIteration:
            return existing_recap_data  # Return if the file is empty
        
        for recap_data_row in reader:
            # Only accounting for the given athlete's data
            if str(recap_data_row["ATHLETE"]).upper() == athlete_name.upper():
                existing_recap_data.update(recap_data_row)
                return existing_recap_data
    print(f"END of query_existing_recap_data() w/ return(s)...\n\texisting_recap_data: {existing_recap_data}\n")
    return existing_recap_data


def update_athlete_recap_data(existing_recap_data, athlete_name, new_athlete_runs):
    """
        Updates the given athlete's recap data.
    """
    print(f"\nSTART of update_athlete_recap_data() w/ arg(s)...\n\texisting_recap_data: {existing_recap_data}\n\tathlete_name: {athlete_name}\n\tnew_athlete_runs: {new_athlete_runs}")

    # TODO: Consolidate below if else, lots of code reuse
    if not existing_recap_data:
        print(f"There is no existing recap data for athlete {athlete_name}. Adding their data...")
        # Adding the new data
        existing_recap_data["ATHLETE"] = athlete_name.upper()
        key_to_find = "DISTANCE (MI)"
        run_distances = [float(d[key_to_find]) for d in new_athlete_runs if key_to_find in d]
        existing_recap_data["TALLIED MILEAGE"] = f"{round(sum(run_distances), 2):.2f}"
        key_to_find = "MOVING TIME"
        run_times = [d[key_to_find] for d in new_athlete_runs if key_to_find in d]
        tallied_time_timedelta, tallied_time_str = tally_time(run_times=run_times)
        existing_recap_data["TALLIED TIME"] = tallied_time_str
        existing_recap_data["# OF RUNS"] = len(new_athlete_runs)
        existing_recap_data["MILEAGE AVG"] = f"{round(float(existing_recap_data["TALLIED MILEAGE"]) / int(existing_recap_data["# OF RUNS"]), 2):.2f}"
        existing_recap_data["TIME AVG"] = divide_time_str_by_number(tallied_time_str, int(existing_recap_data["# OF RUNS"]))
        existing_recap_data["PACE AVG"] = divide_time_str_by_number(tallied_time_str, float(existing_recap_data["TALLIED MILEAGE"]))
        longest_run, longest_run_date = get_longest_run_no_existing_data(new_athlete_runs=new_athlete_runs)
        existing_recap_data["LONGEST RUN"] = longest_run
        existing_recap_data["LONGEST RUN DATE"] = longest_run_date
    else:    
        print(f"Existing recap data was found for athlete {athlete_name}. Updating their data...")
        for col in RECAP_FIELDNAMES:
            print(f"{col}: {existing_recap_data[col]}")
        # Modifying the existing data
        key_to_find = "DISTANCE (MI)"
        run_distances = [float(d[key_to_find]) for d in new_athlete_runs if key_to_find in d]
        existing_recap_data["TALLIED MILEAGE"] = f"{round(float(existing_recap_data["TALLIED MILEAGE"]) + sum(run_distances), 2):.2f}"
        key_to_find = "MOVING TIME"
        run_times = [d[key_to_find] for d in new_athlete_runs if key_to_find in d]
        run_times.append(existing_recap_data["TALLIED TIME"])
        tallied_time_timedelta, tallied_time_str = tally_time(run_times=run_times)
        existing_recap_data["TALLIED TIME"] = tallied_time_str
        existing_recap_data["# OF RUNS"] = int(existing_recap_data["# OF RUNS"]) + len(new_athlete_runs)
        existing_recap_data["MILEAGE AVG"] = f"{round(float(existing_recap_data["TALLIED MILEAGE"]) / int(existing_recap_data["# OF RUNS"]), 2):.2f}"
        existing_recap_data["TIME AVG"] = divide_time_str_by_number(tallied_time_str, int(existing_recap_data["# OF RUNS"]))
        existing_recap_data["PACE AVG"] = divide_time_str_by_number(tallied_time_str, float(existing_recap_data["TALLIED MILEAGE"]))
        longest_run, longest_run_date = get_longest_run(new_athlete_runs=new_athlete_runs, existing_recap_data=existing_recap_data)
        existing_recap_data["LONGEST RUN"] = longest_run
        existing_recap_data["LONGEST RUN DATE"] = longest_run_date
    
    print(f"END of update_athlete_recap_data() w/ return(s)...\n\texisting_recap_data: {existing_recap_data}\n")    
    return existing_recap_data

def handle_any_special_field_updates(activity):
    """
        Checks if a special field has been changed in an activity: title, description, and workout type.

        Args:
            activity (dict): An athlete's activity.
    """
    fieldChanged = [False, False, False]

    # Read the CSV file into a list of dictionaries
    with open(athlete_data_file, 'r', newline='') as data_file:
        reader = csv.DictReader(data_file, fieldnames=ATHLETE_DATA_FIELDNAMES, delimiter=',')
        data = list(reader)

    print(f"This activity already exists in the athlete data file: {activity}")

    # Update the matching row's special fields if they've changed 
    for row in data:
        if row["ACTIVITY ID"] == activity["ACTIVITY ID"]:
            if row["RUN"] != activity["RUN"]:
                fieldChanged[0] = True
                row["RUN"] = activity["RUN"]
            if row["DESCRIPTION"] != activity["DESCRIPTION"]:
                fieldChanged[1] = True
                row["DESCRIPTION"] = activity["DESCRIPTION"]
            if row["WKT TYPE"] != activity["WKT TYPE"]:
                fieldChanged[2] = True
                row["WKT TYPE"] = activity["WKT TYPE"]
            break # Row has been updated, exit this for loop
    
    # Write the updated data back to the CSV file if any fields have changed
    if any(fieldChanged):
        changedFields = [field for field, changed in zip(["TITLE", "DESCRIPTION", "WKT TYPE"], fieldChanged) if changed]
        print(f"The following fields have changed: {', '.join(changedFields)}")
        with open(athlete_data_file, 'w', newline='') as data_file:
            writer = csv.DictWriter(data_file, fieldnames=ATHLETE_DATA_FIELDNAMES)
            writer.writerows(data)

def main():
    """
        Drives all of the main logic.
    """
    # TODO: Simplify this, break the logic apart into helper methods. Too long!!

    # Initialize StravaAPI instances for each athlete
    strava_clients = {}
    for athlete_id, refresh_token in athlete_refresh_tokens.items():
        authorization_client = StravaAuthorization(client_id, client_secret, redirect_uri)
        access_token = authorization_client.exchange_refresh_token(refresh_token)
        strava_clients[athlete_id] = StravaAPI(access_token)

    # Variables
    existing_ids = load_existing_ids(athlete_data_file, unique_column)
    unique_ids = set(existing_ids)

    athlete_count = 0
    # Acquiring new activities to be appended to the relevant CSV files
    for athlete_id, strava_client in strava_clients.items():
        activities = convert_activities_to_list_of_dicts(strava_client.get_activities_this_week(athlete_id))
        rows_added = 0
        if activities:
            for activity in activities:
                # TODO: Update this if conditional (or add another one) to check if we have certain fields updated (see todo list)
                if activity[unique_column] not in unique_ids:
                    cleaned_activity = {key: emoji.demojize(str(value)) if not isinstance(value, str) else emoji.demojize(value) for key, value in activity.items()}
                    rows.append(cleaned_activity)
                    unique_ids.add(cleaned_activity[unique_column])
                    rows_added += 1
                    continue
                else:
                    cleaned_activity = {key: emoji.demojize(str(value)) if not isinstance(value, str) else emoji.demojize(value) for key, value in activity.items()}
                    handle_any_special_field_updates(activity=cleaned_activity)
        else:
            print(f"No activities were retrieved for athlete {athlete_names_parallel_arr[athlete_count]}.")
        print(f"{rows_added} new rows were found for athlete {athlete_names_parallel_arr[athlete_count]}.")
        athlete_count += 1 # Ready for the next athlete
    
    # Sorting all new rows by the "FULL DATETIME" field
    rows.sort(key=lambda x: datetime.strptime(x['FULL DATETIME'], '%Y-%m-%d %H:%M:%S'))
    
    # Append sorted rows to the main ATHLETE_DATA.csv file
    with open(athlete_data_file, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ATHLETE_DATA_FIELDNAMES, delimiter=',')
        if not os.path.exists(athlete_data_file) or os.stat(athlete_data_file).st_size == 0:
            writer.writeheader()
        writer.writerows(rows)
        print(f"{len(rows)} rows were added to {athlete_data_file}.")

    # Update weekly stat and recap files
    recap_rows = list()
    for athlete_name in athlete_names_parallel_arr:
        # Acquiring any new runs
        new_athlete_runs = query_new_runs(rows=rows, athlete_name=athlete_name)

        ### WEEKLY STATS
        # Writing the new athlete X's data to their weekly stats file
        if len(new_athlete_runs) > 0:
            write_athlete_data(new_athlete_runs=new_athlete_runs, athlete_name=athlete_name)

        ### RECAP STATS
        # Querying for existing recap data
        existing_recap_data = query_existing_recap_data(athlete_name=athlete_name)

        # Updating the given athlete's recap data
        if len(new_athlete_runs) > 0:
            recap_rows.append(update_athlete_recap_data(existing_recap_data=existing_recap_data, athlete_name=athlete_name, new_athlete_runs=new_athlete_runs))      
        else:
            if existing_recap_data:
                recap_rows.append(existing_recap_data) # No change in data for this athlete, appending existing data.
    
    # Overwriting the recap data with data in recap_rows
    with open(recap_filename, 'w', newline='') as recap_file:
        # Writing headers if they don't exist
        writer = csv.DictWriter(recap_file, fieldnames=RECAP_FIELDNAMES, delimiter=',')
        if not os.path.exists(recap_filename) or os.stat(recap_filename).st_size == 0:
            writer.writeheader()
        try:
            print(f"Before writing rows: {rows}")
            writer.writerows(recap_rows)
        except Exception as e:
            print(f"Error occurred while writing rows to the recap file: {e}")

main() # Runs every Sunday at 7:30 PM Eastern Standard Time