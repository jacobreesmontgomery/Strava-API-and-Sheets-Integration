import schedule
import time
import os
from dotenv import load_dotenv
import json

load_dotenv()
athlete_names_parallel_arr = json.loads(os.getenv("ATHLETE_NAMES_PARALLEL_ARR"))

def clear_csv(file_path):
    """
        Clears the contents of the specified CSV file.
    """
    with open(file_path, 'w') as file:
        pass  # Opening the file in 'w' mode clears its contents

def clearRecapData():
    # Clearing each athlete's weekly stats
    for athlete in athlete_names_parallel_arr:
        csv_file_path = f"python\code\datasetup\data\weekly_stats\{athlete}_WEEK_STATS.csv"
        clear_csv(csv_file_path)
        print(f"Cleared CSV file at {csv_file_path}.")
    # Clearing the week's recap data
    csv_file_path = r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv"
    clear_csv(csv_file_path)
    print(f"Cleared CSV file at {csv_file_path}.")

clearRecapData()

# Clearance will happen every Monday at 12 AM
schedule.every().monday.at("00:00").do(clearRecapData)

while True:
    schedule.run_pending()
    time.sleep(1)
