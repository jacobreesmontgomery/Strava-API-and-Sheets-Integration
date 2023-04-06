import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import datetime as dt

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('python\client_secret.json', scope)
client = gspread.authorize(creds)

# Opening the Strava API sheet
sheet = client.open("Strava API and Sheets Integration using Apps Script")

# Acquiring the "GOONS" sheet
goons_sheet = sheet.worksheet("GOONS")

### DATA ACQUISITION, CLEANUP, AND SETUP
# Acquiring the activities from the "GOONS" sheet and converting to a column-formatted dataframe
activities = goons_sheet.get_values("A2:P1000")
activities_df = pandas.DataFrame(activities, columns=goons_sheet.get_values("A1:P1"))

# Data cleanup
activities_df[activities_df["WKT TYPE"] == ""]  = "-1" # Updating empty values to -1 (indicating not filled)
activities_df[activities_df["SPM AVG"] == "NA"]  = "-1" # Updating "NA" values to -1 (indicating not filled)
activities_df[activities_df["HR AVG"] == "NA"]  = "-1" # Updating "NA" values to -1 (indicating not filled)

# Data formatting
activities_df[["ATHLETE", "RUN", "DESCRIPTION", "DAY"]] = activities_df[["ATHLETE", "RUN", "DESCRIPTION", "DAY"]].astype("string")
activities_df["ACTIVITY ID"] = activities_df["ACTIVITY ID"].astype("int64")
activities_df[["MONTH", "DATE", "YEAR", "WKT TYPE"]] = activities_df[["MONTH", "DATE", "YEAR", "WKT TYPE"]].astype("int64")
activities_df[["DISTANCE", "SPM AVG", "HR AVG"]] = activities_df[["DISTANCE", "SPM AVG", "HR AVG"]].astype("float")
# Left: MOVING TIME, PACE, and TIME
# TODO: Figure out how tf to convert moving time, pace, and time (we don't just want to take them in as strings)
activities_df["MOVING TIME"] = pandas.to_datetime(activities_df["MOVING TIME"].astype(str), format="%H:%M:%S")
print(activities_df["MOVING TIME"])
# df['est_time'] = df['est_time'].dt.strftime("%H:%M:%S")

# df['Inserted'] = pd.to_datetime(df['Inserted'], format="%m/%d/%Y, %H:%M:%S")

# print(activities_df["SPM AVG"].value_counts()["NA"]) # counts number of "NA" values in the "SPM AVG" column

"""
MOVING TIME	DISTANCE	PACE	FULL DATE	TIME	DAY	MONTH	DATE	YEAR	SPM AVG	HR AVG	WKT TYPE	DESCRIPTION
01:12:04	10.20	00:07:08	4/5/2023	11:13 AM	WED	4	5	2023	NA	157.7	0	20 min tempo 3x(3,2,1) 1 j btw reps 4 j btw sets. Allergy induced coughing made this shitty. Hoping the trees relax soon
"""

### DATA ANALYSIS (MACHINE LEARNING)

