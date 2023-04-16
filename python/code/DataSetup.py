# IMPORTS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import schedule
import time
import datetime

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
    activities_df = pandas.DataFrame(goons_sheet.get_values("A2:P1000"), columns=goons_sheet.get_values("A1:P1"))
    activities_df.to_csv(f"python\data\{sheet_name.upper()}_ACTIVITIES.csv", index=False, sep=",")

    print('Finished the script at {}'.format(datetime.datetime.now())) # Closing print

run_script("Strava API and Sheets Integration using Apps Script", "GOONS")

# Schedule the script to run every day at 8:00 PM
# TODO: Schedule isn't really working, will have to look into it. Some connection issue.
schedule.every().day.at("20:00:00").do(run_script, "Strava API and Sheets Integration using Apps Script", "GOONS")

while True:
    # Run the scheduler
    schedule.run_pending()
    time.sleep(1)