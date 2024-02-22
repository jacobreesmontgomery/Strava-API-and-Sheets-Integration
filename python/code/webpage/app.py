"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

# IMPORTS
from flask import Flask, render_template, send_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import datetime
import csv 

app = Flask(__name__)

# Use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/17178/Documents/Coding Stuff/client_secret.json", scope)
client = gspread.authorize(creds)

# Opening the Strava API sheet
sheet = client.open("Goons Activities - Strava API")

NUM_ATHLETES = 5

# HELPER METHODS
def get_header_stats():
    """
        Return an array containing the columns from the first row
        of the "GOONS RECAP_ACTIVITIES.csv" file.

        Example return:
            [ATHLETE,TALLIED MILEAGE,TALLIED TIME,# OF RUNS,TALLIED ELEVATION,ELEVATION AVG,MILEAGE AVG,TIME AVG,PACE AVG,HR AVG,SPM AVG,LONG RUN,LONG RUN DATE]
    """
    headerStats = []
    with open('python\code\datasetup\data\GOONS RECAP_ACTIVITIES.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headerStats = list(next(reader))
    return headerStats

def get_recap_data():
    """
        Return a 2D array containing the recap data of each athlete, starting
        at row 2 until row X, where X is the last row of the "GOONS RECAP_ACTIVITIES.csv" file.

        Example return:
            [
                [MARK M,09.02,01:12:00,1,00000.0,00000.0,09.02,01:12:00,00:07:59,142.8,#NUM!,-01.00,TBD],
                [ME,07.01,00:50:00,1,00282.2,00282.2,07.01,00:50:00,00:07:08,137.6,167.2,-01.00,TBD]
            ]
    """
    recapData = [[]]
    with open('python\code\datasetup\data\GOONS RECAP_ACTIVITIES.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # Skipping the headers
        for recapRow in reader:
            recapData.append(list(recapRow))
    return recapData

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic_stats')
def basic_stats():
    """
        Drives the rendering of the 'Basic Stats' page with data from "GOONS RECAP_ACTIVITIES.csv."
    """
    return render_template('basic_stats.html', headerStats=get_header_stats(), recapData=get_recap_data())

@app.route('/database')
def database():
    """
        Drives the rendering of the 'Database' page with data from "GOONS_ACTIVITIES.csv."
    """
    # Read in data from the GOONS_ACTIVITIES.csv file and pass it through
    return render_template('database.html')

@app.route('/files/<path:filename>')
def serve_file(filename):
    """
        Allows local files to be referenced via the Flask endpoint.
    """
    directory = 'C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/'
    return send_file(directory + '/' + filename)

if __name__ == '__main__':
    app.run(debug=True)