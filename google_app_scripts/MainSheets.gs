/**
 * A time-triggered function which retrieves my activities for the "ME" sheet.
 */
function getMyActivities() {
  // get the sheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('ME');

  // Grabbing current IDs from
  var currActivities = grabCurrentEntryIDs(5, 1, sheet);

  // call the Strava API to retrieve data
  var data = callStravaActivitiesAPI("ME");

  // empty array to hold activity data
  var newActivities = [];
  var haveNewRun = false;

  // loop over activity data and add to newActivities array for Sheet
  if (data.length > 0) {
    data.forEach(
      function(activity) {
          var activityConverted = [];

          // if the given activity is not contained within the current sheet, add it
          if (!currActivities.includes(activity.id) && activity.type == "Run") {
            haveNewRun = true;

            // Converting moving time from seconds to the format of HH:MM:SS
            var date = new Date(null);
            date.setSeconds(activity.moving_time);
            var movingTime = date.toISOString().substring(11, 18);

            // Example start_date_local: 2023-02-22T17:02:39Z
            // Future desired functionality: Parsing of start_date_local into a date (YYYY-MM-DD) column and time (HH:MM:SS) column
            //    Note: Currently, I've just established formatting on the sheet
            var startTimestampOfRun = activity.start_date_local;
            var dateOfRun = startTimestampOfRun.substring(0,10);
            var timeOfRun = startTimestampOfRun.substring(11, 19);

            activityConverted.push(
              activity.id,
              activity.name,
              movingTime,
              Math.round((activity.distance/1609 + Number.EPSILON) * 100) / 100,
              dateOfRun,
              timeOfRun
            );
            newActivities.push(activityConverted);
          }
        }
    );
  } else Logger.log('No activities were pulled.');

  // paste the values into the Sheet
  if (haveNewRun) {
    sheet.insertRowsBefore(5, newActivities.length).getRange(5, 1, newActivities.length, newActivities[0].length).setValues(newActivities);
    Logger.log(`Inserted ${newActivities.length} new rows for the given athlete: ${JSON.stringify(newActivities, null, 2)}`);
  }
  else Logger.log('There are no new activities.');
}

/**
 * This time-triggered function-run at 10-11AM and 7-8PM every day--gets all 
 *    the activities of my goons (specified in AthleteTokens.gs), sorted by Date.
 * 
 * TODO: Big limitation that we need to resolve: The data request limits - 100 requests every 15 minutes, 1,000 daily.
 *          The reason for Patrick's data not being grabbed is because by the time the other athlete's data
 *          is retrieved, we've reached our cap, so we end up coming empty for Patrick L as a result. We're hitting
 *          that 100 request threshold in the span of an execution... Limit data to 100 / NUM_GOONS per API call.
 *       Of course, the other, long-term solution which I want eventually either way is the webhook subscription setup.
 *          Only downside to that is that it won't check for changes to the description. Only picks up updates
 *          to the title, privacy, or type. However, you get the activity ID returned, so I can use that to 
 *          check on the description as well. Doubt the rest of the fields would auto-update, but I'll have to dig into it.
 */
function getGoonsRuns() {
  Logger.log(`================START OF getGoonsRuns()================`);

  // get the sheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('GOONS');

  // Grabbing current IDs from the "GOONS" sheet and establishing boolean to track if anything changes in the "GOONS" sheet
  var currActivities = grabCurrentEntryIDs(START_ROW_OF_ACTIVITIES_GOONS_SHEET, 2, sheet);
  var goonsSheetChangeMade = false;

  // Iterating over my goons (index 0 is me)
  for (var i = 1; i < ATHLETE_NAMES.length; i++) {
    var goon = ATHLETE_NAMES[i];

    // Call the Strava API to retrieve data
    var data = callStravaActivitiesAPI(goon);
    
    // Empty array to hold activity data and boolean to track if modifications were made
    var newActivities = [];
    var newActivity = false;

    if (data.length > 0) {
      // Iterating over the given goon's activities
      data.forEach(
        function(activity) {
          var currActivity = sheet.getRange(START_ROW_OF_ACTIVITIES_GOONS_SHEET, 1, sheet.getLastRow(), getNumberOfHeaders(sheet, START_ROW_OF_HEADERS_GOONS_SHEET, 1)).getValues().filter((run) => run[1] == activity.id); 
          Logger.log(`\nExisting activity: ${JSON.stringify(currActivity, null, 2)}`)
          var activityConverted = parseIncomingActivity(activity, goon); // gets the data into a format for appending to the "GOONS" sheet
          if (activity.type != "Run") {
            Logger.log(`Activity ${activity.id} for ${goon} will NOT be processed as it is NOT a run. Moving on to the next activity...`);
          } else if (!currActivities.includes(activity.id)) {
            newActivity = true; // We have an activity which must be added
            Logger.log(`Activity ${activity.id} for ${goon} will be processed as it is NOT in the "GOONS" sheet.`);
            newActivities.push(activityConverted); // Adding the converted activity to the list of newActivities
          } else {
            Logger.log(`Activity ${activity.id} for ${goon} already exists in the "GOONS" sheet. Checking if changes have been made...`);
            // Format of valueChangesArr: [T/F, [T/F, T/F, T/F, T/F], [ID, "name", "wkt_type", "description"]]
            var valueChangesArr = haveDynamicValuesChanged(currActivity, [activityConverted]);
            if (valueChangesArr[0]) {
              Logger.log(`Modifications must be made. Making the modifications...`);
              modifyRun(valueChangesArr[1], valueChangesArr[2], activity.id, "GOONS");
            } else {
              Logger.log(`Modifications will NOT be made. Moving on to the next activity...`);
            }
          }
        }
      );
    } else Logger.log(`No activities were acquired for ${goon}.`);
    
    Logger.log(`The new activities for ${goon} to add... ${JSON.stringify(newActivities, null, 2)}`);
    // Adding the goon's new activities to the sheet
    if (newActivity) {
      goonsSheetChangeMade = true;
      sheet.getRange(sheet.getLastRow() + 1, 1, newActivities.length, newActivities[0].length).setValues(newActivities);
      Logger.log(`Inserted ${newActivities.length} new activities for ${goon}: ${JSON.stringify(newActivities, null, 2)}`);
    }
  }

  // Sorting all of the activities by columns FULL DATE and TIME after checking on all my goon's activities
  if (goonsSheetChangeMade) sheet.getRange(START_ROW_OF_ACTIVITIES_GOONS_SHEET, 1, sheet.getLastRow(), getNumberOfHeaders(sheet, START_ROW_OF_HEADERS_GOONS_SHEET, 1)).sort([{column: 7, ascending: false}, {column: 8, ascending: false}]);
  else Logger.log(`No changes to the "GOONS" sheet are needed upon execution of getGoonsRuns()...`);
  Logger.log(`================END OF getGoonsRuns()================`);
}

/**
 * BELOW ARE THE HELPER METHODS.
 */

/**
 * Parses the incoming activity data into an array.
 * 
 * @param activity, the incoming activity 
 * @param goon, the given athlete
 * 
 * @return an array containing the parsed data
 */
function parseIncomingActivity(activity, goon) {
  var detailedActivity = callStravaActivityIdAPI(goon, activity.id);
  var activityConverted = [];
  
  // Acquiring moving time and distance run
  var date = new Date(null);
  date.setSeconds(activity.moving_time);
  var movingTime = date.toISOString().substring(11, 18);
  var distRun = (activity.distance * 0.000621371).toFixed(2);    

  // Acquiring date and time of run (from start_date_local)
  var startTimestampOfRun = activity.start_date_local;
  var dateOfRun = startTimestampOfRun.substring(0,10);
  var timeOfRun = startTimestampOfRun.substring(11, 19);

  // Acquiring day, month, year of run
  date = new Date(activity.start_date_local).getDate(); 
  var day = (new Date(activity.start_date_local)).getDay();
  switch (day) {
    case 0:
      day = "SUN";
      break;
    case 1:
      day = "MON";
      break;
    case 2:
      day = "TUE";
      break;
    case 3:
      day = "WED";
      break;
    case 4:
      day = "THU";
      break;
    case 5:
      day = "FRI";
      break;
    case 6:
      day = "SAT";
      break;
    default:
      day = "???";
      break;
  }
  var month = new Date(activity.start_date_local).getMonth() + 1;
  var year = new Date(activity.start_date_local).getFullYear();

  // Acquiring pace (from average_speed)
  var avgPace = 60/(activity.average_speed * 2.23694).toFixed(2); // gets whole number w/ decimals
  var paceSeconds = (avgPace % 1 * 60).toFixed(0); // gets decimal places
  if (paceSeconds.length == 1) paceSeconds = `0${paceSeconds}`; // adds a 0 if we're in the single digits (0-9 seconds)
  var paceMinutes = (avgPace - (avgPace % 1)).toFixed(0);
  if (paceMinutes.length == 1) paceMinutes = `0${paceMinutes}`; // adds a 0 if we're in the single digits (0-9 minutes)
  var pace = `00:${paceMinutes}:${paceSeconds}`;
  if (isNaN(paceMinutes) && isNaN(paceSeconds)) pace = "NA";
  
  // Acquiring average cadence and average heartrate, if they exist
  var avgCadence = activity.average_cadence * 2;
  if (isNaN(avgCadence)) avgCadence = "NA";

  var avgHR = activity.average_heartrate;
  if (!avgHR) avgHR = "NA";

  // Appending the acquired values to the final array to be returned
  activityConverted.push(
    goon,
    activity.id,
    activity.name,
    movingTime,
    distRun,
    pace,
    dateOfRun,
    timeOfRun,
    day,
    month, 
    date,
    year,
    avgCadence,
    avgHR, 
    activity.workout_type,
    detailedActivity.description
  );

  return activityConverted;
}

/**
 * Determines if any of the dynamic values have changed for the given athlete's activity from the "GOONS" sheet.
 * 
 * @param existingActivity, the activity already in the "GOONS" sheet (double array)
 * @param incomingActivity, the incoming activity (double array) that matches the existingActivity ID
 * 
 * @return -1 if an issue comes up, true if any of the dynamic values have changed, and false otherwise
 */
function haveDynamicValuesChanged(existingActivity, incomingActivity) {
  var existingActivityMapped = existingActivity.map((run) => [run[1], run[2], run[14], run[15]]).flat();
  var incomingActivity = incomingActivity.map((run) => [run[1], run[2], run[14], run[15]]).flat();
  // Updating null values to be empty for the incoming activity
  for (var i = 0; i < incomingActivity.length; i++) {
    if (incomingActivity[i] == null) {
      incomingActivity[i] = "";
    }
  }
  
  if (existingActivityMapped.length != incomingActivity.length) {
    Logger.log(`Invalid inputs: The activities must match in length. Existing activity length = ${existingActivityMapped.length} but incoming activity length = ${incomingActivity.length}. Exiting...`);
    return -1;
  }

  var mustModifyRowInSheet = false;
  var modifyDynamicValues = [false, false, false, false];
  var modifyDynamicValuesTo = [, "", "", ""];
  for (var i = 0; i < existingActivityMapped.length; i++) {
    if (existingActivityMapped[i] != incomingActivity[i]) {
      mustModifyRowInSheet = true;
      if (i == 0) Logger.log(`The ID of the run, currently ${existingActivityMapped[i]}, will be updated to ${incomingActivity[i]}.`);
      else if (i == 1) Logger.log(`The name of the run, currently ${existingActivity[i]}, will be updated to ${incomingActivity[i]}.`);
      else if (i == 2) Logger.log(`The workout type of the run, currently ${existingActivity[i]}, will be updated to ${incomingActivity[i]}.`);
      else Logger.log(`The description of the run, currently ${existingActivity[i]}, will be updated to ${incomingActivity[i]}.`);
      // Modifying arrays to indicate we need to modify the given activity value in the "GOONS" sheet 
      modifyDynamicValues[i] = true;    
      modifyDynamicValuesTo[i] = incomingActivity[i];
    }
  }

  return [mustModifyRowInSheet, modifyDynamicValues, modifyDynamicValuesTo];
}

/**
 * Modifies the given run for the given athlete.
 * 
 * @param modifyDynamicValues, a parallel array containing booleans representing whether to modify a given value or not
 * @param modifyDynamicValuesTo, the parallel array containing values representing what to change the given values to
 * @param activityID, the ID of the activity on which we are making modification(s) 
 * @param sheetName, the name of the sheet on which to make modifications
 */
function modifyRun(modifyDynamicValues, modifyDynamicValuesTo, activityID, sheetName) {
  // Acquiring the activity's row to modify
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  var currRow = -1, rowOfActivity = -1;
  if (sheetName == "GOONS") currRow = START_ROW_OF_HEADERS_GOONS_SHEET;
  else currRow = 1; 

  getAthletesRunsFromThisWeek(sheet, sheetName).map(run => run[1]).forEach((runID) => {
    currRow++;
    if (runID == activityID) {
      rowOfActivity = currRow;
      Logger.log(`Found a match at row ${rowOfActivity} for ID ${runID}.`);
    }
  });  

  // Overwriting the relevant values (0 => activity ID, 1 => run (name), 2 => wkt_type, 3 => description)
  Logger.log(`Overwriting the relevant values at row ${rowOfActivity}...`);
  if (modifyDynamicValues[0]) sheet.getRange(rowOfActivity, 2).setValue(modifyDynamicValuesTo[0]);
  if (modifyDynamicValues[1]) sheet.getRange(rowOfActivity, 3).setValue(modifyDynamicValuesTo[1]);
  if (modifyDynamicValues[2]) sheet.getRange(rowOfActivity, 15).setValue(modifyDynamicValuesTo[2]);
  if (modifyDynamicValues[3]) sheet.getRange(rowOfActivity, 16).setValue(modifyDynamicValuesTo[3]);
}

/**
 * Gets the number of (non-empty) headers for the given sheet, startRow, and startCol.
 * 
 * @param sheet, the sheet we'd like to inspect
 * @param startRow, the row we'd like to start the range at
 * @param startCol, the column we'd like to start the range at
 * 
 * @return an integer representing the length of the resulting array
 */
function getNumberOfHeaders(sheet, startRow, startCol) {
  return sheet.getRange(startRow, startCol, 1, sheet.getMaxColumns()).getValues().flat().filter((col) => col).length;
}

/**
 * Grabs the current populated entries for the given sheet starting at row startingRow
 * 
 * @param startingRow, the row we'd like to start the range at
 * @param activityIdCol, the activity ID column we want to inspect
 * @param sheet, the sheet we'd like to grab entry IDs from
 * 
 * @return a list of activity IDs
 */
function grabCurrentEntryIDs(startingRow, activityIdCol, sheet) {
  return sheet.getRange(startingRow, activityIdCol, sheet.getLastRow(), 1).getValues().flat();
}

/**
 * Calls on the /athlete/activities endpoint of the Strava API and
 *  retrieves a list of activities for the given athlete.
 * 
 * @param athlete, the given athlete we'd like to fetch activities from
 * 
 * @return a list of activities
 */
function callStravaActivitiesAPI(athlete) {   
  // set up the service
  var service = getStravaService();
  
  if (service.hasAccess()) {
    var params = `?per_page=${Math.floor(100 / NUM_OF_ACTIVE_GOONS).toFixed(0)}`;
    // Possible issue: Could still hit data limit cap because we also fetch for the DetailedActivity
    // Another idea: Change to the after parameter with per_page limit of 10. Establish after to be the start of the current week.

    // Acquiring access token for the given athlete
    var accessToken = getNewAccessToken(ATHLETE_TOKENS[ATHLETE_NAMES.indexOf(athlete)], athlete);

    var endpoint = `https://www.strava.com/api/v3/athlete/activities${params}`;

    var response = fetchActivityRequest(endpoint, accessToken);
    return response;
  }
  else {
    Logger.log("App has no access yet.");
     
    // open this url to gain authorization from github
    var authorizationUrl = service.getAuthorizationUrl();
     
    Logger.log("Open the following URL and re-run the script: %s",
        authorizationUrl);
  }
}

/**
 * Calls on the /activities/{id} endpoint of the Strava API and
 *  retrieves detailed information (DetailedActivity) for the given athlete's activity ID.
 * 
 * @param athlete, the athlete to fetch DetailedActivity data from
 * @param id, the ID of the desired activity
 * 
 * @return a DetailedActivity object
 */
function callStravaActivityIdAPI(athlete, id) {   
  // set up the service
  var service = getStravaService();
   
  if (service.hasAccess()) {        
    // Acquiring access token for the given athlete
    var accessToken = getNewAccessToken(ATHLETE_TOKENS[ATHLETE_NAMES.indexOf(athlete)], athlete);

    var endpoint = `https://www.strava.com/api/v3/activities/${id}`;

    var response = fetchActivityRequest(endpoint, accessToken);
    return response;
  }
  else {
    Logger.log("App has no access yet.");
     
    // open this url to gain authorization from github
    var authorizationUrl = service.getAuthorizationUrl();
     
    Logger.log("Open the following URL and re-run the script: %s",
        authorizationUrl);
  }
}

/**
 * Acquires a new, fresh access token for the given athlete.
 * */
function getNewAccessToken(refreshToken, athlete) {
  var service = getStravaService();

  var endpoint = `https://www.strava.com/oauth/token?client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&refresh_token=${refreshToken}&grant_type=refresh_token`;
  var accessToken = fetchAccessToken(endpoint);
  
  return accessToken.access_token;
}

/**
 * Fetches the constantly-refreshing access token for the given endpoint.
 */
function fetchAccessToken(endpoint) {
    Logger.log('Starting fetch request for endpoint = ' + endpoint);
    
    var options = {
      method : 'POST',
      muteHttpExceptions: true
    };
     
    var response = JSON.parse(UrlFetchApp.fetch(endpoint, options));

    return response;
}

/**
 * Fetches the relevant activities for the given endpoint.
 */
function fetchActivityRequest(endpoint, accessToken) {
    Logger.log('Starting fetch request for endpoint = ' + endpoint);

    var headers = {
      Authorization: 'Bearer ' + accessToken
    };
    
    var options = {
      headers: headers,
      method : 'GET',
      muteHttpExceptions: true
    };
    
    var response = JSON.parse(UrlFetchApp.fetch(endpoint, options));

    return response;
}