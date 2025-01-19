from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from os import environ

from services.strava_api import StravaAuthorization, StravaAPI
from dao.strava_activities_dao import StravaActivitiesDao
from dao.strava_athlete_dao import StravaAthleteDao
from dao.services.database_service import DatabaseService

new_athlete_router = APIRouter()

# VARIABLES
load_dotenv()
CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
REDIRECT_URI = environ.get("REDIRECT_URI")
AUTH_EXCHANGE_LINK = environ.get("AUTH_EXCHANGE_LINK")

# Initialize database services
db_service = DatabaseService()
athlete_db_engine = StravaAthleteDao(db_service=db_service)
activities_db_engine = StravaActivitiesDao(db_service=db_service)


class NewAthletesAPI:
    """
    Handles authorization of new athletes.
    """

    @new_athlete_router.get("/new-athlete/redirect")
    async def redirect(self, request: Request):
        return RedirectResponse(AUTH_EXCHANGE_LINK)

    @new_athlete_router.get("/new-athlete")
    async def root(self, request: Request):
        code = request.query_params.get("code")
        if code:
            return await self.callback(code=code)
        return {"message": "Welcome to the Strava OAuth Integration"}

    @new_athlete_router.get("/new-athlete/callback")
    async def callback(self, request: Request, code: str):
        try:
            # Complete authorization
            auth = StravaAuthorization(CLIENT_ID, CLIENT_SECRET, f"{REDIRECT_URI}")

            # Acquire a refresh token
            token_response = auth.exchange_authorization_code(code)
            access_token = token_response["access_token"]
            refresh_token = token_response["refresh_token"]

            # Acquire athlete information with the access token
            client = StravaAPI(access_token=access_token)
            athlete_data = client.get_athlete_data()
            if not athlete_data:
                return {"message": "Failed to retrieve athlete information"}
            athlete_id = athlete_data.id
            athlete_name = f"{athlete_data.firstname} {athlete_data.lastname}"
            athlete_email = athlete_data.email

            # Upsert the athlete's data to the strava_api.athletes DB table
            rows_affected = athlete_db_engine.upsert_athlete(
                athlete_id=athlete_id,
                athlete_name=athlete_name,
                refresh_token=refresh_token,
                email=athlete_email,
            )
            if rows_affected > 0:
                message = "You have been successfully authenticated!"
                message_type = "success"
            else:
                message = "Authentication failed. Please try again."
                message_type = "error"
        except Exception as e:
            message = "Authentication failed."
            message_type = "error"

        redirect_url = f"http://localhost:3000/new-athlete-result?message={message}&message_type={message_type}"
        return RedirectResponse(redirect_url)
