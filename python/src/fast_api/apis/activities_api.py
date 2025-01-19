from fastapi import APIRouter, Request

activities_router = APIRouter()


class ActivitiesAPI:
    """
    Handles all activities API requests.
    """

    @activities_router.get("/activities/basic-stats")
    async def get_activities(self, request: Request):
        """
        Retrieves all activities for the authenticated athlete.
        """
        # TODO: Implement this method
        pass

    @activities_router.get("/activities/detailed-stats")
    async def get_detailed_activities(self, request: Request):
        """
        Retrieves detailed statistics for all activities for the authenticated athlete.
        """
        # TODO: Implement this method
        pass
