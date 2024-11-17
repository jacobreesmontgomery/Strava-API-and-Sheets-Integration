"""
This is a utility for upserting activity data from the ATHLETE_DATA.csv 
file into the strava_api.activities DB table.
"""
from csv import reader as CSVReader
import sys
import os

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, package_path)
from DatabaseService import DatabaseService
from StravaActivitiesDao import StravaActivitiesDao
from StravaAthleteDao import StravaAthleteDao

def process_csv(csv_file_path):
    db_service = DatabaseService()
    activity_dao = StravaActivitiesDao(db_service)
    athlete_dao = StravaAthleteDao(db_service)

    with open(csv_file_path, mode='r') as file:
        reader = CSVReader(file)
        next(reader)  # skip header row

        # TODO - JACOB: Debug what's going on during the get_athlete_id call via the debugger

        for row in reader:
            # We have to acquire the ID via this DB call because the ATHLETE_DATA file doesn't have the ID
            athlete_id = athlete_dao.get_athlete_id(athlete_name=row[0]) if row[0] and len(row[0]) > 0 else None
            if athlete_id is None:
                print(f"Athlete '{row[0]}' not found in the database. Skipping this activity...")
                continue # skip this activity
            
            print(f"Athlete '{row[0]}' was found in the database. Establishing data to be inserted...")
            print(f"Row of length {len(row)}: {row}")
            print(f"Wkt type: '{row[14]}'")
            # Parse row data (modify the indices based on the CSV structure)
            activity_data = (
                int(athlete_id),  # athlete_id
                row[0],           # athlete
                int(row[1]),      # activity_id
                row[2],           # run
                row[3],           # moving_time
                float(row[4]),    # distance_mi
                row[5],           # pace_min_mi
                row[6],           # full_date
                row[7],           # time
                row[8],           # day
                int(row[9]),      # month
                int(row[10]),     # date
                int(row[11]),     # year
                float(row[12]) if row[12] != "N/A" else row[12],   # spm_avg (float or "N/A")
                float(row[13]) if row[13] != "N/A" else row[13],   # hr_avg (float or "N/A")
                int(row[14]) if row[14] not in (None, 'None', '') else -1,                # wkt_type
                row[15],          # description
                float(row[16]),   # total_elev_gain_ft
                row[17] == 'True',# manual (convert string to boolean)
                float(row[18]),   # max_speed_ft_s
                float(row[19]),   # calories
                int(row[20]),     # achievement_count
                int(row[21]),     # kudos_count
                int(row[22]),     # comment_count
                int(row[23]),     # athlete_count
                row[24],          # full_datetime
                int(row[25]) if row[25] not in ("N/A", "") else row[25],     # rpe (int or "N/A")
                int(row[26]) if row[26] not in ("N/A", "") else row[26],     # rating (int or "N/A")
                int(row[27]) if row[27] not in ("N/A", "") else row[27],     # avg_power (int or "N/A")
                int(row[28]) if row[28] not in ("N/A", "") else row[28]      # sleep_rating (int or "N/A")
            )
            activity_dao.upsert_activity(activity_data)
            print("Activity data inserted successfully.")

if __name__ == "__main__":
    csv_file_path = r'C:\Users\17178\Desktop\GITHUB_PROJECTS\Strava-API-and-Sheets-Integration\python\code\datasetup\data\main_data\ATHLETE_DATA.csv'
    process_csv(csv_file_path)
