# Strava-API-and-Sheets-Integration

This is a front-end web-based Python application which will pull data from the GOONS_ACTIVITIES.csv file--updated daily by this app's DataSetup.py file--and do various things with that data such as data visualization, data analysis, etc.

## Pages

### Main Page

This page will include a few things...

1. A card component for each athlete that can be clicked on to go to specific stats and data visualizations for the given athlete.
2. A link to a 'Basic Stats' page.
3. A link to a 'Database' page.

### Athlete Data

This page will hold specific data to the athlete selected on the main page. A user will only be directed to this page if they click on a card component from the main page.

### Basic Stats

This page will hold basic week recap stats. This will be pulled from the "GOONS RECAP" sheet.

### Database

This page will have a filterable table to hold all runs stored in the "GOONS_ACTIVITIES.csv" file referenced above. The user will be able to filter by all columns.

## App startups

Follow these steps to get everything up and running:

1. In one terminal, navigate to the front-end-react directory and run `npm start`.
2. In another terminal, navigate to the Node server, `server.js`, and run `npm start`.
3. In a third terminal, navigate to the FastAPI backend, `app.py`, and run one of two commands:
   - Reload on code changes: `uvicorn app:app --reload`
   - No reload: `TBD`
