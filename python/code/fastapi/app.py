"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

# IMPORTS
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
import os
import sys
from logging import basicConfig, INFO, getLogger
from dotenv import load_dotenv

# Setup logging
basicConfig(level=INFO)
logger = getLogger(__name__)

# Ensure the correct path for imports
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, package_path)
from datasetup.api.StravaAPI import StravaAuthorization, StravaAPI
from code.dao.StravaAthleteDao import StravaAthleteDao
from code.dao.DatabaseService import DatabaseService

# Load environment variables
load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
AUTH_EXCHANGE_LINK = os.environ.get('AUTH_EXCHANGE_LINK')

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the database service and athlete db engine
db_service = DatabaseService()
athlete_db_engine = StravaAthleteDao(db_service=db_service)

ATHLETE_WEEK_RECAP_CSV = "C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/datasetup/data/recap/ATHLETE_WEEK_RECAP.csv"
ATHLETE_DATA_CSV = "C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/datasetup/data/main_data/ATHLETE_DATA.csv"

### HELPER METHODS ###
# TODO - Once everything below is refactored, get rid of these helper methods
def get_header_stats(csvFile: str) -> list[str]:
    """
        Return an array containing the columns from the first row
        of the csvFile file.
    """

    headerStats = []
    try:
        with open(csvFile) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            headerStats = list(next(reader))
    except Exception as e:
        logger.error(f"Error reading CSV file {csvFile}: {e}")
    return headerStats


def get_row_data(csvFile: str) -> list[list[str]]:
    rowData = []
    try:
        with open(csvFile) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)  # Skipping the headers
            for row in reader:
                rowData.append(list(row))
    except Exception as e:
        logger.error(f"Error reading CSV file {csvFile}: {e}")
    return rowData


def update_env_file(athlete_refresh_tokens, athlete_names):
    env_file_path = "C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/.env"
    try:
        logger.info(f"Incoming args:\nATHLETE_REFRESH_TOKENS: {athlete_refresh_tokens}\nATHLETE_NAMES_PARALLEL_ARR: {athlete_names}")

        # Convert the dictionaries and lists to properly formatted strings
        athlete_refresh_tokens_str = str(athlete_refresh_tokens).replace("'", '"')
        athlete_names_str = str(athlete_names).replace("'", '"')
                
        with open(env_file_path, "r") as file:
            lines = file.readlines()
        
        with open(env_file_path, "w") as file:
            for line in lines:
                if line.startswith("ATHLETE_REFRESH_TOKENS"):
                    file.write(f'ATHLETE_REFRESH_TOKENS={athlete_refresh_tokens_str}\n')
                elif line.startswith("ATHLETE_NAMES_PARALLEL_ARR"):
                    file.write(f'ATHLETE_NAMES_PARALLEL_ARR={athlete_names_str}\n')
                else:
                    file.write(line)
    except Exception as e:
        logger.error(f"Error updating .env file: {e}")


### ENDPOINTS ###
@app.get("/api/basic-stats")
async def basic_stats():
    """
        Drives the rendering of the 'Basic Stats' page with data from "ATHLETE_WEEK_RECAP.csv."
    """
    # TODO - Rework to make DB GET calls
    headerStats = get_header_stats(ATHLETE_WEEK_RECAP_CSV)
    rowData = get_row_data(ATHLETE_WEEK_RECAP_CSV)
    return {"headerStats": headerStats, "rowData": rowData}


@app.get("/api/database")
async def database():
    """
        Drives the rendering of the 'Database' page with data from "ATHLETE_DATA.csv."
    """
    # TODO - Rework to make DB GET calls
    headerStats = get_header_stats(ATHLETE_DATA_CSV)
    rowData = get_row_data(ATHLETE_DATA_CSV)
    return {"headerStats": headerStats, "rowData": rowData}


@app.get("/api/strava_auth")
async def strava_auth():
    logger.info(f"Redirecting to Strava Auth URL: {AUTH_EXCHANGE_LINK}")
    return RedirectResponse(AUTH_EXCHANGE_LINK)


@app.get("/")
async def root(request: Request):
    logger.info(f"Received request to the root endpoint: {request}")
    code = request.query_params.get("code")
    if code:
        return await callback(code=code)
    return {"message": "Welcome to the Strava OAuth Integration"}


@app.get("/api/callback")
async def callback(code: str):
    logger.info(f"Callback received with code: {code}")
    try:
        # Complete authorization 
        auth = StravaAuthorization(CLIENT_ID, CLIENT_SECRET, f"{REDIRECT_URI}")
        
        # Acquire a refresh token
        token_response = auth.exchange_authorization_code(code)
        logger.info(f"Exchanged authorization code for token: {token_response}")
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']

        # Acquire athlete information with the access token
        client = StravaAPI(access_token=access_token)
        athlete_data = client.get_athlete_data()
        if not athlete_data:
            logger.error("Failed to retrieve athlete information")
            return {"message": "Failed to retrieve athlete information"}
        logger.info(f"Retrieved athlete information: {athlete_data}")
        athlete_id = athlete_data.id
        athlete_name = f"{athlete_data.firstname} {athlete_data.lastname}"
        athlete_email = athlete_data.email

        # Upsert the athlete's data to the strava_api.athletes DB table
        rows_affected = athlete_db_engine.upsert_athlete(athlete_id=athlete_id, athlete_name=athlete_name, refresh_token=refresh_token, email=athlete_email)
        if rows_affected > 0:
            message = "You have been successfully authenticated!"
            message_type = "success"
            logger.info("Successfully inserted the athlete's data to the strava_api.athletes DB table")
        else: 
            message = "Authentication failed. Please try again."
            message_type = "error"
            logger.error(f"Error during athlete data insertion to strava_api.athletes: {e}")
    except Exception as e:
        message = "Authentication failed."
        message_type = "error"
        logger.error(f"Error during callback: {e}")

    redirect_url = f"http://localhost:3000/auth-result?message={message}&message_type={message_type}"
    return RedirectResponse(redirect_url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)