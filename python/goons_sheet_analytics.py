import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('python\client_secret.json', scope)
client = gspread.authorize(creds)

# Opening the Strava API sheet
sheet = client.open("Strava API and Sheets Integration using Apps Script")

# Acquiring the "GOONS" sheet
goons_sheet = sheet.worksheet("GOONS")

# Acquiring the activities from the "GOONS" sheet and converting to a column-formatted dataframe
activities = goons_sheet.get_values("A2:P1000")
activities_df = pandas.DataFrame(activities, 
                                columns=goons_sheet.get_values("A1:P1"))
print(activities_df.dtypes) # Printing the dataframe types


