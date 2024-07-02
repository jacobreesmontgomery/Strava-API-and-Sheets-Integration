"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

# IMPORTS
from flask import Flask, render_template, send_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv 

app = Flask(__name__)

# Use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/17178/Documents/Coding Stuff/client_secret.json", scope)
client = gspread.authorize(creds)

# Opening the Strava API sheet
sheet = client.open("Goons Activities - Strava API")

# HELPER METHODS
def get_header_stats(csvFile):
    """
        Return an array containing the columns from the first row
        of the csvFile file.

        Example return for csvFile "ATHLETE_WEEK_RECAP.csv":
            [ATHLETE,TALLIED MILEAGE,TALLIED TIME,# OF RUNS,TALLIED ELEVATION,ELEVATION AVG,MILEAGE AVG,TIME AVG,PACE AVG,HR AVG,SPM AVG,LONG RUN,LONG RUN DATE]
    """
    headerStats = []
    with open(csvFile) as csvfile:
        print('Before reader initialization')
        reader = csv.reader(csvfile, delimiter=',')
        print('After reader intialization')
        headerStats = list(next(reader))
        print('After headeStats initialization')
    print(f"END of get_header_stats() w/ return(s)...\n\theaderStats: {headerStats}")
    return headerStats

def get_row_data(csvFile):
    """
        Return a 2D array containing the data of each row, starting
        at row 2 until row X, where X is the last row of the csvFile file.

        Example return for csvFile "ATHLETE_WEEK_RECAP.csv":
            [
                [MARK M,09.02,01:12:00,1,00000.0,00000.0,09.02,01:12:00,00:07:59,142.8,#NUM!,-01.00,TBD],
                [ME,07.01,00:50:00,1,00282.2,00282.2,07.01,00:50:00,00:07:08,137.6,167.2,-01.00,TBD]
            ]
    """
    rowData = [[]]
    with open(csvFile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # Skipping the headers
        for row in reader:
            rowData.append(list(row))
    print(f"END of get_row_stats() w/ return(s)...\n\trowData: {rowData}")
    return rowData

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic_stats')
def basic_stats():
    """
        Drives the rendering of the 'Basic Stats' page with data from "ATHLETE_WEEK_RECAP.csv."
    """
    return render_template(
        'basic_stats.html', 
        headerStats=get_header_stats(r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv"), 
        rowData=get_row_data(r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv")
    )

@app.route('/database')
def database():
    """
        Drives the rendering of the 'Database' page with data from "ATHLETE_DATA.csv."
    """
    # TODO: Fix this method. Looks like the fields are populating, they're just not populating to the database page.
    # might be an issue with the renderer / script being used.

    # Read in data from the ATHLETE_DATA.csv file and pass it through
    return render_template(
        'database.html', 
        headerStats=get_header_stats(r"python\code\datasetup\data\main_data\ATHLETE_DATA.csv"), 
        rowData=get_row_data(r"python\code\datasetup\data\main_data\ATHLETE_DATA.csv")
    )

@app.route('/files/<path:filename>')
def serve_file(filename):
    """
        Allows local files to be referenced via the Flask endpoint.
    """
    directory = 'C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/'
    return send_file(directory + '/' + filename)

if __name__ == '__main__':
    app.run(debug=True)