"""
CLASS: DataSetup.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file is designed to pull run data from a spreadsheet 
            and write it to a CSV file on which data analysis can be done
            within the DataAnalysis.ipynb file.
"""

# IMPORTS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import datetime

# GLOBAL VARIABLES
NUM_ATHLETES = 6 # TODO: Make this dynamic

# METHOD(S)
def run_script(spreadsheet, sheet_name):
    """
        Authorizes this script with the Google Drive API using our credentials
        and transfers the data from the "GOONS" sheet to a CSV file: GoonsActivities.

        @param spreadsheet, the spreadsheet we want to open
        @param sheet_name, the name of the sheet we'd like to extract data from
    """
    print('Starting the script at {}'.format(datetime.datetime.now())) # Opening print

    # Use creds to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/17178/Documents/Coding Stuff/client_secret.json", scope)
    client = gspread.authorize(creds)

    # Opening the Strava API sheet
    sheet = client.open(spreadsheet)

    # Acquiring the sheet activities and writing the data to a CSV file
    goons_sheet = sheet.worksheet(sheet_name)
    if (sheet_name == "GOONS"): 
        activities_df = pandas.DataFrame(goons_sheet.get_values(f"A2:P10000"), columns=goons_sheet.get_values("A1:P1"))
    elif (sheet_name == "GOONS RECAP"):
        activities_df = pandas.DataFrame(goons_sheet.get_values(f"A4:{3 + NUM_ATHLETES}"), columns=goons_sheet.get_values("A3:M3"))
    activities_df.to_csv(f"python\code\datasetup\data\main_data\{sheet_name.upper()}_ACTIVITIES.csv", index=False, sep=",")
    
    print('Finished the script at {}'.format(datetime.datetime.now())) # Closing print

# Calling to retrieve data from the "GOONS" sheet and inject into a CSV file
run_script("Goons Activities - Strava API", "GOONS")
run_script("Goons Activities - Strava API", "GOONS RECAP")