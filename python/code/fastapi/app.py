"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

# IMPORTS
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from typing import List
import os
import sys
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the correct path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datasetup.api.StravaAPI import StravaAuthorization, StravaAPI

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

# Use creds to create a client to interact with the Google Drive API
try:
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/17178/Documents/Coding Stuff/client_secret.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Goons Activities - Strava API")
except Exception as e:
    logger.error(f"Failed to authorize Google Sheets client: {e}")
    raise


ATHLETE_WEEK_RECAP_CSV = "C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/datasetup/data/recap/ATHLETE_WEEK_RECAP.csv"
ATHLETE_DATA_CSV = "C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/datasetup/data/main_data/ATHLETE_DATA.csv"

### HELPER METHODS ###
def get_header_stats(csvFile: str) -> List[str]:
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


def get_row_data(csvFile: str) -> List[List[str]]:
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
    headerStats = get_header_stats(ATHLETE_WEEK_RECAP_CSV)
    rowData = get_row_data(ATHLETE_WEEK_RECAP_CSV)
    return {"headerStats": headerStats, "rowData": rowData}


@app.get("/api/database")
async def database():
    """
        Drives the rendering of the 'Database' page with data from "ATHLETE_DATA.csv."
    """
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
        logging.info(f"Exchanged authorization code for token: {token_response}")
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']

        # Acquire athlete information with the access token
        client = StravaAPI(access_token=access_token)
        athlete_data = client.get_athlete_data()
        logging.info(f"Retrieved athlete information: {athlete_data}")
        athlete_id = str(athlete_data['id'])
        athlete_name = athlete_data['firstname'] + ' ' + athlete_data['lastname']
        logging.info(f"Received access token [{access_token}], refresh token [{refresh_token}], athlete ID [{athlete_id}], and name [{athlete_name}].")

        # Update the .env file with the new information (if it's actually new)
        entries_exist = False
        ATHLETE_REFRESH_TOKENS = os.getenv("ATHLETE_REFRESH_TOKENS", "{}")
        ATHLETE_REFRESH_TOKENS = eval(ATHLETE_REFRESH_TOKENS)
        if athlete_id and refresh_token and not ATHLETE_REFRESH_TOKENS.get(athlete_id):
            ATHLETE_REFRESH_TOKENS[athlete_id] = refresh_token
            os.environ["ATHLETE_REFRESH_TOKENS"] = str(ATHLETE_REFRESH_TOKENS).replace("'", '"')
        else:
            logging.info(f"The entry for athlete [{athlete_id}] already exists in the .env variable ATHLETE_REFRESH_TOKENS.")
            entries_exist = True

        ATHLETE_NAMES_PARALLEL_ARR = os.getenv("ATHLETE_NAMES_PARALLEL_ARR", "[]")
        ATHLETE_NAMES_PARALLEL_ARR = eval(ATHLETE_NAMES_PARALLEL_ARR)
        if athlete_name and not entries_exist: # Assuming if the above doesn't exist, this won't.
            ATHLETE_NAMES_PARALLEL_ARR.append(athlete_name)
            os.environ["ATHLETE_NAMES_PARALLEL_ARR"] = str(ATHLETE_NAMES_PARALLEL_ARR).replace("'", '"')
        else:
            logging.info(f"The entry for athlete [{athlete_id}] already exists in the .env variable ATHLETE_NAMES_PARALLEL_ARR.")

        if not entries_exist: 
            logging.info(f"Calling on update_env_file()")
            update_env_file(ATHLETE_REFRESH_TOKENS, ATHLETE_NAMES_PARALLEL_ARR)
            logging.info(f"Updated the .env file.")
        
        message = "You have been successfully authenticated!"
        message_type = "success"
    except Exception as e:
        message = "Authentication failed."
        message_type = "error"
        logger.error(f"Error during callback: {e}")

    redirect_url = f"http://localhost:3000/auth-result?message={message}&message_type={message_type}"
    return RedirectResponse(redirect_url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)