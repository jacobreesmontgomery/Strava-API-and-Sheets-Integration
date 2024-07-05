"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

# IMPORTS
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/17178/Documents/Coding Stuff/client_secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Goons Activities - Strava API")

### HELPER METHODS ###
def get_header_stats(csvFile: str) -> List[str]:
    """
        Return an array containing the columns from the first row
        of the csvFile file.
    """
    headerStats = []
    with open(csvFile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headerStats = list(next(reader))
    return headerStats

def get_row_data(csvFile: str) -> List[List[str]]:
    """
        Return a 2D array containing the data of each row, starting
        at row 2 until row X, where X is the last row of the csvFile file.
    """
    rowData = []
    with open(csvFile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skipping the headers
        for row in reader:
            rowData.append(list(row))
    return rowData

### ENDPOINTS ###
@app.get("/api/basic-stats")
async def basic_stats():
    """
        Drives the rendering of the 'Basic Stats' page with data from "ATHLETE_WEEK_RECAP.csv."
    """
    headerStats = get_header_stats(r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv")
    rowData = get_row_data(r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv")
    return {"headerStats": headerStats, "rowData": rowData}

@app.get("/api/database")
async def database():
    """
        Drives the rendering of the 'Database' page with data from "ATHLETE_DATA.csv."
    """
    headerStats = get_header_stats(r"python\code\datasetup\data\main_data\ATHLETE_DATA.csv")
    rowData = get_row_data(r"python\code\datasetup\data\main_data\ATHLETE_DATA.csv")
    return {"headerStats": headerStats, "rowData": rowData}

@app.get("/files/{filename:path}")
async def serve_file(filename: str):
    """
        Allows local files to be referenced via the FastAPI endpoint.
    """
    directory = 'C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/'
    file_path = f"{directory}/{filename}"
    try:
        return FileResponse(file_path)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
