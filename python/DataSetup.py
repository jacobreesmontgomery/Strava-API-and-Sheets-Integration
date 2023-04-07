import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/17178/Documents/Coding Stuff/client_secret.json", scope)
client = gspread.authorize(creds)

# Opening the Strava API sheet
sheet = client.open("Strava API and Sheets Integration using Apps Script")

# Acquiring the "GOONS" sheet activities and writing to "GoonsActivities.csv"
goons_sheet = sheet.worksheet("GOONS")
activities_df = pandas.DataFrame(goons_sheet.get_values("A2:P1000"), columns=goons_sheet.get_values("A1:P1"))
activities_df.to_csv("python\data\GoonsActivities.csv", index=False, sep=",")