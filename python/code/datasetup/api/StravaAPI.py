from stravalib.client import Client
from stravalib.exc import RateLimitExceeded
from datetime import datetime, timedelta
from stravalib.client import Client

class StravaAuthorization:
    """
        Responsible for authorization of a given athlete and acquiring their newest access token.
    """
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = Client()

    def get_authorization_url(self):
        return self.client.authorization_url(client_id=self.client_id, redirect_uri=self.redirect_uri)
    
    def exchange_refresh_token(self, refresh_token):
        token_response = self.client.refresh_access_token(client_id=self.client_id, client_secret=self.client_secret, refresh_token=refresh_token)
        return token_response['access_token']
    
    def exchange_authorization_code(self, code):
        token_response = self.client.exchange_code_for_token(client_id=self.client_id, client_secret=self.client_secret, code=code)
        return token_response

class StravaAPI:
    """
        Responsible for making calls to the Strava API for activity data.
    """
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = Client(access_token)

    def get_activities_this_week(self, athlete_id):
        """
        Gets the atlete's activities for the current week.

        Args:
            athlete_id: The athlete's ID

        Returns:
            List[Activity]: A list of the current week's activities
        """
        try:
            # Calculate the start and end of the current week in UTC
            today = datetime.now()
            start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_week = (start_of_week + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999)
            # Retrieve activities within the current week
            activities = self.client.get_activities(after=start_of_week, before=end_of_week)
            activity_ids_and_type = [(activity.id, activity.type) for activity in activities]
            detailed_activities = list()
            for activity_id, activity_type in activity_ids_and_type:
                if activity_type == "Run": # Only including runs
                    detailed_activities.append(self.client.get_activity(activity_id=activity_id))
            return detailed_activities
        except RateLimitExceeded:
            print("Strava API rate limit exceeded. Please try again later.")
            return None
        except Exception as e:
            print(f"Failed to retrieve this week's activities for athlete {athlete_id}.")
            return None
    
    def get_activities(self, athlete_id: int, start_date: str = None, end_date: str = None):
        """
        Gets the athlete's activities for a default, or specified, timeframe.

        Args:
            athlete_id: The athlete's ID
            start_date: The start date, as an epoch timestamp, of the timeframe for activities (optional)
            end_date: The end date, as an epoch timestamp, of the timeframe for activities (optional)

        Returns:
            List[Activity]: A list of activities for the specified athlete and timeframe.
        """
        try:
            activities = None
            if start_date and end_date:
                activities = self.client.get_activities(after=start_date, before=end_date)
            elif start_date:
                activities = self.client.get_activities(after=start_date)
            elif end_date:
                activities = self.client.get_activities(before=end_date)
            else:
                activities = self.client.get_activities()
            return list(activities)
        except Exception as e:
            print(f"Failed to retrieve activities for athlete ID {athlete_id}: {e}")
            return None
        
    def get_athlete_data(self):
        """
        Gets the athlete's basic information via the /athlete endpoint.
        """
        try:
            athlete_data = self.client.get_athlete()
            return dict(athlete_data)
        except Exception as e:
            print(f"An error occurred while retrieving athlete data: {e}")
            return None
