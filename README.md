# Strava-API-and-Sheets-Integration

This BFF-architected application takes advantage of the Strava API to acquire running data on authenticated athletes and present it in valuable ways to the users.

## Pages

### Main Page

This page will be comprised of...

1. A card component for each athlete that can be clicked on to go to specific stats and data visualizations for the given athlete.
2. A menu linking the following...
   1. A 'Basic Stats' page.
   2. A 'Database' page.
   3. A 'Chat' page.

### Athlete Data

This page will hold specific data to the athlete selected on the main page. A user will only be directed to this page if they click on a card component from the main page.

### Basic Stats

This page will hold basic week recap stats, pulled from the `strava_api.activities` DB table.

### Database

This page will have a filterable table to hold all runs stored in the `strava_api.activities` DB table. The user will be able to filter by all columns.

### Chat

In a traditional chatbot interface, the user will be able to ask questions about their training and receive intelligent, GenAI-driven answers.

## App startups

Follow these steps to get everything up and running:

1. Ensure you're using the virtual environment: `.venv\Scripts\Activate.ps1`.
2. In one terminal, navigate to the front-end-react directory and run `npm start`.
3. In another terminal, navigate to the Node server, `server.js`, and run `npm start`.
4. In a third terminal, navigate to the FastAPI backend, `app.py`, and run one of two commands:
   - Reload on code changes: `uvicorn app:app --reload`
   - No reload: `TBD`

## GENERAL APP FLOW

### AUTHENTICATION FLOW
1. A user authenticates with the app by clicking the 'Authenticate' button on the FE.
2. The request is routed from the FE to the BE NodeJS server, `server.js`.
3. The NodeJS server receives the request and routes it to the BE FastAPI server.
4. The BE FastAPI endpoint receives the request and adds the newly authenticated user to the `strava_api.athletes` DB table.
5. Going forward, the new user's activities will be acquired on a scheduled frequency, going into the `strava_api.activities` DB table while also being presented on one of the website's pages.