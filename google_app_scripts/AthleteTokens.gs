// FOR IMPORTANT GLOBALLY-REFERENCED VARIABLES
AUTH_EXCHANGE_LINK='https://www.strava.com/oauth/authorize?client_id=83199&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all'; // This one is how I get the code with which to retrieve the refresh token for my athletes

TIMMY_B_REFRESH_TOKEN = 'ed67f6258bfd8ad0851a4d5c544d0766432ab9e8'; // Done his training, add him back to ATHLETE* arrays once he's back
PAIGE_O_REFRESH_TOKEN = '0726964a5a1735551ccee68f46e7df753b9bebb4';
MARK_M_REFRESH_TOKEN = '23d1f3b6f426daf584d6cce3987fff9b2443ff0c';
DAVID_L_REFRESH_TOKEN = 'e9a8cf64fd7d49df41d5aca427c9dc77a3ed7409';
PATRICK_L_REFRESH_TOKEN = '25a0a96e7a6f57bd393c8e76fc83c68486289790';
TAD_D_REFRESH_TOKEN = '';
MY_REFRESH_TOKEN = 'e62f800366085277ebdb8a54c81a6306f9b01fa9';

// Establishing parallel arrays
NUM_OF_ACTIVE_GOONS=4; // update as athletes stop/start new training blocks
ATHLETE_NAMES=['ME', 'PATRICK L', 'PAIGE O', 'MARK M', 'DAVID L']; // The list of my current athletes (which can also be found in The Goon Squad)
ATHLETE_TOKENS=[MY_REFRESH_TOKEN, PATRICK_L_REFRESH_TOKEN, PAIGE_O_REFRESH_TOKEN, MARK_M_REFRESH_TOKEN, DAVID_L_REFRESH_TOKEN];

// Essential variables for the sheets
RECAP_STATS_HEADERS_GOONS_RECAP=["ATHLETE", "TALLIED MILEAGE", "TALLIED TIME", "# OF RUNS", "MILEAGE AVG", "TIME AVG", "PACE AVG", "LONG RUN", "LONG RUN DATE"];
RECAP_STATS=["TALLIED MILEAGE", "TALLIED TIME", "# OF RUNS", "MILEAGE AVG", "TIME AVG", "PACE AVG", "LONG RUN", "LONG RUN DATE"];
NUM_OF_RECAP_STATS=RECAP_STATS.length;
ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS=7;
ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STAT_HEADERS=ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS-1;

WORKOUT_RECAP_STATS_GOONS_RECAP=["ATHLETE", "WKT #", "WKT ID", "RUN",  "DESCRIPTION",	"FULL DATE", "DAY",	"TIME"];
WORKOUT_RECAP_STATS=["WKT #", "WKT ID", "RUN",  "DESCRIPTION",	"FULL DATE", "DAY",	"TIME"];
NUM_OF_WORKOUT_RECAP_STATS=WORKOUT_RECAP_STATS.length;
ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS=ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS+3;
ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS_HEADERS=ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS-1;

ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET=3;
ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_HEADER=4;
ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_STATS=ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_HEADER+1;

// GOONS SHEET
START_ROW_OF_HEADERS_GOONS_SHEET=1;
START_ROW_OF_ACTIVITIES_GOONS_SHEET=START_ROW_OF_HEADERS_GOONS_SHEET+1;

/*
JSON RESPONSE BODIES FOR INITIAL APP AUTHENTICATION
---------------------------------------------------

TIMMY B
{
    "token_type": "Bearer",
    "expires_at": 1677576044,
    "expires_in": 21600,
    "refresh_token": "ed67f6258bfd8ad0851a4d5c544d0766432ab9e8",
    "access_token": "2843a6f19fc696f06162fce5550321ff507f7667",
    "athlete": {
        "id": 37088575,
        "username": null,
        "resource_state": 2,
        "firstname": "Timmy",
        "lastname": "Buzynski",
        "bio": "CYHS 18 YCP 22",
        "city": "Philadelphia ",
        "state": "Pennsylvania",
        "country": "United States",
        "sex": "M",
        "premium": false,
        "summit": false,
        "created_at": "2018-12-11T16:11:36Z",
        "updated_at": "2023-02-27T21:41:37Z",
        "badge_type_id": 0,
        "weight": 0.0,
        "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/37088575/12264838/1/medium.jpg",
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/37088575/12264838/1/large.jpg",
        "friend": null,
        "follower": null
    }
}

PAIGE O
{
    "token_type": "Bearer",
    "expires_at": 1677650763,
    "expires_in": 21600,
    "refresh_token": "0726964a5a1735551ccee68f46e7df753b9bebb4",
    "access_token": "cc2b6ca5f5cfc5ad1c076eb36ff4e6185aa4c5be",
    "athlete": {
        "id": 38344933,
        "username": "paige_ottaviano",
        "resource_state": 2,
        "firstname": "Paige",
        "lastname": "Ottaviano",
        "bio": null,
        "city": "Pittsburgh ",
        "state": "Pennsylvania",
        "country": "United States",
        "sex": "F",
        "premium": true,
        "summit": true,
        "created_at": "2019-01-16T00:59:36Z",
        "updated_at": "2023-03-01T00:02:15Z",
        "badge_type_id": 1,
        "weight": 0.0,
        "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/38344933/12830201/7/medium.jpg",
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/38344933/12830201/7/large.jpg",
        "friend": null,
        "follower": null
    }
}

MARK M
{
    "token_type": "Bearer",
    "expires_at": 1677651293,
    "expires_in": 21600,
    "refresh_token": "23d1f3b6f426daf584d6cce3987fff9b2443ff0c",
    "access_token": "dc467247087a399d613a752b8ea23d02e355cb34",
    "athlete": {
        "id": 79510728,
        "username": null,
        "resource_state": 2,
        "firstname": "Mark",
        "lastname": "Magee",
        "bio": null,
        "city": null,
        "state": null,
        "country": null,
        "sex": "M",
        "premium": true,
        "summit": true,
        "created_at": "2021-02-26T16:25:43Z",
        "updated_at": "2023-03-01T00:09:52Z",
        "badge_type_id": 1,
        "weight": 0.0,
        "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/79510728/19154363/1/medium.jpg",
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/79510728/19154363/1/large.jpg",
        "friend": null,
        "follower": null
    }
}

DAVID L
{
    "token_type": "Bearer",
    "expires_at": 1677652499,
    "expires_in": 21600,
    "refresh_token": "e9a8cf64fd7d49df41d5aca427c9dc77a3ed7409",
    "access_token": "24615b7050e4b3c24a870dc7d8c46c9eecd7d00d",
    "athlete": {
        "id": 48964720,
        "username": "david_lefkowitz",
        "resource_state": 2,
        "firstname": "David",
        "lastname": "Lefkowitz",
        "bio": "Reasonably Speedy | Voted Hermitage HS JV Boys' Volleyball's \"Most Improved\", October 2014  |  Tortuga!",
        "city": "Richmond",
        "state": "VA",
        "country": null,
        "sex": "M",
        "premium": false,
        "summit": false,
        "created_at": "2019-12-15T02:30:21Z",
        "updated_at": "2023-01-10T17:11:52Z",
        "badge_type_id": 0,
        "weight": 74.8427,
        "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/48964720/15595982/5/medium.jpg",
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/48964720/15595982/5/large.jpg",
        "friend": null,
        "follower": null
    }
}

PATRICK L

*/