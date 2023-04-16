/**
 * This time-triggered function creates sheets for each unique athlete (if their sheet doesn't exist already)
 *    and populates their sheets with their activities from the current week.
 * 
 * TODO: Might want to update this to reflect our additional columns. 
 */
function createAthleteSheetsIfNotExists() {
    var goonsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS");
    var allSheets = getAllSheets();
    var uniqueAthletesList = getListOfUniqueAthletes(goonsSheet);
  
    // Determining whether each athlete needs a spreadsheet or not
    uniqueAthletesList.forEach(
      function(athlete) {
        // If there is not a sheet for the given athlete, we want to create that sheet and establish formatting and initial values
        if (!allSheets.includes(athlete)) {
          Logger.log(`We do not have a sheet for ${athlete}. Creating sheet...`);
          var newAthleteSheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet();
          newAthleteSheet.setName(`${athlete}`);
  
          // Adding headers from the "GOONS" sheet to the new sheet and establishing column formatting
          newAthleteSheet.appendRow(goonsSheet.getRange(START_ROW_OF_HEADERS_GOONS_SHEET, 1, 1, getNumberOfHeaders(goonsSheet, START_ROW_OF_HEADERS_GOONS_SHEET, 1)).getValues().flat());
          newAthleteSheet.getRange("D2:D10000").setNumberFormat("hh:mm:ss"); // format for moving time
          newAthleteSheet.getRange("E2:E10000").setNumberFormat("00.00"); // format for distance
          newAthleteSheet.getRange("F2:F10000").setNumberFormat("hh:mm:ss"); // format for pace
          newAthleteSheet.getRange("H2:H10000").setNumberFormat("hh:mm:ss AM/PM"); // format for time
  
          // Copying over headers from "GOONS" sheet to the new athlete sheet
          var numHeaders = getNumberOfHeaders(goonsSheet, START_ROW_OF_HEADERS_GOONS_SHEET, 1);
          goonsSheet.getRange(START_ROW_OF_HEADERS_GOONS_SHEET, 1, 1, numHeaders).copyTo(newAthleteSheet.getRange(1, 1, 1, numHeaders));
  
          // Populate with their activities from the "GOONS" sheet
          var athleteActivities = getAthletesRunsFromThisWeek(goonsSheet, athlete);
          if (athleteActivities.length > 0) newAthleteSheet.getRange(2, 1, athleteActivities.length, athleteActivities[0].length).setValues(athleteActivities);
  
          // Adding the statistics view with the current data
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STAT_HEADERS, 1, 2, NUM_OF_RECAP_STATS).setBorder(true, true, true, true, true, true);
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STAT_HEADERS, 1, 1, NUM_OF_RECAP_STATS).setBackground("lightgrey").setValues([RECAP_STATS]).setFontWeight("bold");
  
          // Setting values and formatting
          var athleteStats = [];
          if (athleteActivities.length > 0) {
            athleteStats = getAthleteStats(newAthleteSheet);
            newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 1, 1, athleteStats[0].length).setValues(athleteStats);
          }
  
          // Basic week recap: TALLIED MILEAGE	TALLIED TIME	# OF RUNS	MILEAGE AVG	TIME AVG	PACE AVG	LONG RUN	LONG RUN DATE
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 1, 1, 1).setNumberFormat("00.00");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 2, 1, 1).setNumberFormat("hh:mm:ss");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 3, 1, 1).setNumberFormat("0");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 4, 1, 1).setNumberFormat("00.00");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 5, 1, 1).setNumberFormat("hh:mm:ss");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 6, 1, 1).setNumberFormat("hh:mm:ss");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 7, 1, 1).setNumberFormat("00.00");
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 8, 1, 1).setNumberFormat("MM/dd/yyyy");
  
          // Workouts recap: WKT #	RUN	DESCRIPTION	FULL DATE	DAY	TIME
          var athleteSheetWeeksWorkouts = [];
          if (athleteActivities.length > 0) {
            athleteSheetWeeksWorkouts = getWorkoutStatsFromAthleteSheet(newAthleteSheet);
            if (athleteSheetWeeksWorkouts.length > 0) {
              Logger.log(`${athlete} has ${athleteSheetWeeksWorkouts.length} marked workouts.`);
              // Adding workout # to the start of the array
              var wktCount = 0;
              athleteSheetWeeksWorkouts.forEach((workouts) => {
                wktCount++;
                workouts.unshift(`${wktCount}`); 
              });
              // Adding the workout(s) data to the workout recap section
              newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 1, athleteSheetWeeksWorkouts.length, athleteSheetWeeksWorkouts[0].length).setValues(athleteSheetWeeksWorkouts).sort({column: 5, ascending: true});
  
              // Formatting necessary cells for workout details
              newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 1, athleteSheetWeeksWorkouts.length, 1).setNumberFormat("0");
              newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 5, athleteSheetWeeksWorkouts.length, 1).setNumberFormat("MM/dd/yyyy");
              newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 7, athleteSheetWeeksWorkouts.length, 1).setNumberFormat("hh:mm:ss AM/PM");
            } else Logger.log(`${athlete} has ${athleteSheetWeeksWorkouts.length} marked workouts.`);
          }
  
          // Headers and formatting
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS_HEADERS, 1, 1, NUM_OF_WORKOUT_RECAP_STATS).setValues([WORKOUT_RECAP_STATS]);
          if (athleteSheetWeeksWorkouts.length > 0) newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS_HEADERS, 1, 1 + athleteSheetWeeksWorkouts.length, NUM_OF_WORKOUT_RECAP_STATS).setBorder(true, true, true, true, true, true);
          else newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS_HEADERS, 1, 2, NUM_OF_WORKOUT_RECAP_STATS).setBorder(true, true, true, true, true, true);
          newAthleteSheet.getRange(1 + athleteActivities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS_HEADERS, 1, 1, NUM_OF_WORKOUT_RECAP_STATS).setBackground("lightgrey").setValues([WORKOUT_RECAP_STATS]).setFontWeight("bold");
  
          // Aligning all cells to left-justified
          newAthleteSheet.getRange(1, 1, newAthleteSheet.getLastRow(), numHeaders).setHorizontalAlignment("left");
        } else Logger.log(`There is already a sheet for ${athlete}`);
      }
    )
  }
  
  /**
   * This time-triggered function, run every day at 8-9PM EST, will update the given athlete's 
   *    sheet with their new activities from the "GOONS" sheet for the current week.
   * */
  function updateAthleteSheets() {
    var goonsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS");
  
    // Checking on each athlete's sheets and making sure they're up-to-date with the "GOONS" sheet
    getListOfUniqueAthletes(goonsSheet).forEach(
      function(athlete) {
        // Acquiring activities for the given athlete from both the "GOONS" sheet and their designated sheet
        var athletesRunsThisWeek = getAthletesRunsFromThisWeek(goonsSheet, athlete);
        var athleteSheetActivityIDs = getIDsFromAthleteSheet(athlete);
        if (athleteSheetActivityIDs != -1) {
          Logger.log(`${athlete}'s run IDs from their sheet: ${JSON.stringify(athleteSheetActivityIDs, null, 2)}`);
          var athleteSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(athlete);        
          var activitiesToAddToAthleteSheet = athletesRunsThisWeek.filter((activity) => !athleteSheetActivityIDs.includes(activity[1]));
  
          // If we have new activities, add them to the athlete's sheet
          if (activitiesToAddToAthleteSheet.length > 0) {
            Logger.log(`Adding ${activitiesToAddToAthleteSheet.length} activities to ${athlete}'s sheet: ${JSON.stringify(activitiesToAddToAthleteSheet, null, 2)}`);
            athleteSheet.insertRowsBefore(2, activitiesToAddToAthleteSheet.length).getRange(2, 1, activitiesToAddToAthleteSheet.length, activitiesToAddToAthleteSheet[0].length).setValues(activitiesToAddToAthleteSheet);
  
            // Updating the week's statistics
            var athleteStats = getAthleteStats(athleteSheet);
            athleteSheet.getRange(1 + getActivitiesFromAthleteSheet(athleteSheet).length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 1, 1, athleteStats[0].length).setValues(athleteStats);
  
            // Updating the week's workout statistics
            var athleteSheetWeeksWorkouts = getWorkoutStatsFromAthleteSheet(athleteSheet);
            Logger.log(`${athlete} has ${athleteSheetWeeksWorkouts.length} newly marked workouts.`);
            if (athleteSheetWeeksWorkouts.length > 0) {
              // Adding workout # to the start of the array
              var wktCount = 0;
              athleteSheetWeeksWorkouts.forEach((workouts) => {
                wktCount++;
                workouts.unshift(`${wktCount}`); 
              });
              // Adding the workout(s) data to the workout recap section
              athleteSheet.getRange(1 + getActivitiesFromAthleteSheet(athleteSheet).length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 1, athleteSheetWeeksWorkouts.length, athleteSheetWeeksWorkouts[0].length).setValues(athleteSheetWeeksWorkouts).sort({column: 4, ascending: true});
              athleteSheet.getRange(1 + getActivitiesFromAthleteSheet(athleteSheet).length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 1, athleteSheetWeeksWorkouts.length, athleteSheetWeeksWorkouts[0].length).setBorder(true, true, true, true, true, true);
            }
          } else Logger.log(`${athlete} has no new activities. Checking if any dynamic values have changed in the 'GOONS' sheet...`);
          
          // If a dynamic value has changed for an activity, modify the run in the athlete sheet
          var athleteSheetActivities = getActivitiesFromAthleteSheet(athleteSheet);
          for (var i = 0; i < athletesRunsThisWeek.length; i++) {
            var valuesChangedArr = haveDynamicValuesChanged([athleteSheetActivities[i]], [athletesRunsThisWeek[i]]);
            if (valuesChangedArr[0]) {
              valueChanged = true;
              Logger.log(`Modifications must be made to activity ${athleteSheetActivities[i][1]} of WKT_TYPE ${athleteSheetActivities[i][14]}. Making the modifications...`);
              modifyRun(valuesChangedArr[1], valuesChangedArr[2], athletesRunsThisWeek[i][1], athlete);
              
              // If we've modified a workout entry, modify the corresponding workout stat
              if (parseInt(athletesRunsThisWeek[i][14]) == "3") {
                // Filtering down to a matching workout
                var athleteSheetWorkout = getWorkoutStatsFromAthleteSheet(athleteSheet).filter((wkt) => (wkt[0] == athletesRunsThisWeek[i][1]));
                if (athleteSheetWorkout.length > 0) {
                  // Updating the workout data in the workout recap section
                  var wktNum = 0;
                  for (var wktRow = 1 + getActivitiesFromAthleteSheet(athleteSheet).length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS; wktRow <= athleteSheet.getLastRow(); wktRow++) {
                    wktNum++;
                    // If we have a match between WKT ID and ACTIVITY ID, modify the given workout stats
                    if (athleteSheet.getRange(wktRow, 2).getValue() == athletesRunsThisWeek[i][1]) {
                      athleteSheetWorkout[0].unshift(`${wktNum}`);
                      Logger.log(`Workout #${wktNum} being modified to...\n${JSON.stringify(athleteSheetWorkout[0], null, 2)}`);
                      athleteSheet.getRange(wktRow, 1, 1, NUM_OF_WORKOUT_RECAP_STATS).setValues([athleteSheetWorkout[0]]);
                      break; // Exiting as we've found our match and remove 
                    }
                  }           
                }
              }
            } else {
              Logger.log(`Modifications will NOT be made to activity ${athleteSheetActivities[i]}. Moving on to the next activity...`);
            }
          }
          athleteSheet.getRange(1, 1, athleteSheet.getLastRow(), athleteSheet.getLastColumn()).setHorizontalAlignment("left");
        } else Logger.log("Moving on to the next athlete...");
      }
    );
  }
  
  /**
   * This time-triggered function--run every Monday at 12-1AM--clears out activities NOT from the current week for each athlete's sheet. 
   *  Because of when this is run, it's really just wiping the athlete sheet clean to start a new week.
   */
  function clearOldActivities() {
    getAthleteSheets().forEach((sheet) => {
      // Removing activities not from the current week for the given sheet
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheet);
      var activities = getActivitiesFromAthleteSheet(sheet);
      var numWorkouts = 0;
      if (activities.length > 0) numWorkouts = getWorkoutStatsFromAthleteSheet(sheet).length;
      Logger.log(`The activities acquired for athlete ${sheet.getName()}...`); Logger.log(activities);
  
      // Clearing summary (and workout) content
      sheet.getRange(1 + activities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 1, 1, NUM_OF_RECAP_STATS).clearContent();
      if (numWorkouts > 0) sheet.getRange(1 + activities.length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 1, numWorkouts, NUM_OF_WORKOUT_RECAP_STATS).clearContent(); 
  
      // Clearing activities
      for (var i = activities.length - 1; i >= 0; i--) {
        var activity = activities[i];
        if (!getDatesFromCurrentWeek().includes(formatDate(activity[6]))) {
          Logger.log(`The following activity is NOT in the current week and should be removed:\n${JSON.stringify(activity, null, 2)}`);
          Logger.log(`Removing row ${i + 2}`);
          sheet.deleteRow(i + 2);
        } else Logger.log(`The following activity is in the current week and should NOT be removed:\n${JSON.stringify(activity, null, 2)}`);
      }
    });
  }
  
  /*
    NOTE: BELOW ARE THE HELPER METHODS.
  */
  
  /**
   * Gets the workout statistics for the given athlete from their sheet.
   */
  function getWorkoutStatsFromAthleteSheet(sheet) {
    return sheet.getRange(2, 1, getActivitiesFromAthleteSheet(sheet).length, getNumberOfHeaders(sheet, 1, 1)).getValues().filter((run) => run[14] == 3).map(run => [run[1], run[2], run[15], formatDate(run[6]), run[8], run[7]]).reverse();
  }
  
  /**
   * Gets the workout statistics for the given athlete from the "GOONS" sheet.
   */
  function getWorkoutStatsFromGoonsSheet(athlete) {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS");
    var datesFromThisWeek = getDatesFromCurrentWeek();
    return sheet.getRange(START_ROW_OF_ACTIVITIES_GOONS_SHEET, 1, sheet.getLastRow(), getNumberOfHeaders(sheet, START_ROW_OF_HEADERS_GOONS_SHEET, 1)).getValues().filter((run) => datesFromThisWeek.includes(formatDate(run[6])) && run[0] == athlete && run[14] == 3).map(run => [run[2], run[15], formatDate(run[6]), run[8], run[7]]);
  }
  
  /**
   * This function acquires the activities from a given athlete's sheet.
   * 
   * @return an integer representing the number of activities
   */
  function getActivitiesFromAthleteSheet(sheet) {
    return sheet.getRange(2, 1, sheet.getLastRow(), getNumberOfHeaders(sheet, 1, 1)).getValues().filter((row) => row[0] == sheet.getSheetName());
  }
  
  /**
   * Gets the statistics for the given athlete.
   * 
   * @return a list containing the tallied mileage, number of runs, and average miles per run.
   */
  function getAthleteStats(sheet) {
    var talliedMileage = 0, numOfRuns = 0, avgMilesPerRun = 0, timeAvg = 0, paceAvg = 0, longRun = -1, numWorkouts = 0;
    var talliedTime = new Date("Sat Dec 30 1899 00:00:00 GMT-0500 (Eastern Standard Time)"); // Establishing date with 00:00:00 for hh:mm:ss
    var talliedPace = new Date("Sat Dec 30 1899 00:00:00 GMT-0500 (Eastern Standard Time)"); // Establishing date with 00:00:00 for hh:mm:ss
    var longRunDate = "TBD";
  
    // Tallying up time, mileage, pace, and number of runs
    getActivitiesFromAthleteSheet(sheet).map((run) => [run[3], run[4], run[5]]).forEach((keyStats) => {
        // keyStats[0] = MOVING TIME, keyStats[1] = DISTANCE, keyStats[2] = PACE
        talliedTime = addTimes(parseDuration(talliedTime), parseDuration(keyStats[0]));
        talliedTime = new Date(`Sat Dec 30 1899 ${talliedTime} GMT-0500 (Eastern Standard Time)`);
        talliedMileage += parseFloat(keyStats[1]); // Have to convert the String to a Float to add mileage
        talliedPace = addTimes(parseDuration(talliedPace), parseDuration(keyStats[2]));
        talliedPace = new Date(`Sat Dec 30 1899 ${talliedPace} GMT-0500 (Eastern Standard Time)`); 
        numOfRuns++;
      }
    );
  
    // Final calculations before returning
    timeAvg = getDividedTime(talliedTime, numOfRuns);
    paceAvg = getDividedTime(talliedPace, numOfRuns);
    talliedTime = parseDuration(talliedTime);
    talliedPace = parseDuration(talliedPace);
    avgMilesPerRun = (talliedMileage / numOfRuns).toFixed(2);
    if (isLastDayOfWeek()) {
      var longRunArr = getAthletesLongRun(sheet);
      longRun = longRunArr[0];
      longRunDate = longRunArr[1];
    }
    numWorkouts = getWorkoutStatsFromGoonsSheet(sheet.getSheetName()).length;
  
    // Logging and returning the statistics
    Logger.log(`TOTAL MILEAGE: ${talliedMileage}\nTOTAL TIME: ${talliedTime}\n# RUNS: ${numOfRuns}\nAVG MPR: ${avgMilesPerRun}\nTIME AVG: ${timeAvg}\nPACE AVG: ${paceAvg}\nLR: ${longRun}\nLR DATE: ${longRunDate}\n# WKTS: ${numWorkouts}`);
    return [[talliedMileage, talliedTime, numOfRuns, avgMilesPerRun, timeAvg, paceAvg, longRun, longRunDate]];
  }
  
  /**
   * This function gets the longest run (distance and date) for the given athlete every Sunday at 8-9PM EST.
   */
  function getAthletesLongRun(sheet) {
    var longestRun = 0;
    var longestRunDate = "";
    
    getAthletesRunsFromThisWeek(sheet, sheet.getSheetName()).map(run => [run[4], formatDate(run[6])]).forEach((run) => {
      // run[0] = distance, run[1] = date
      if (run[0] > longestRun) {
        longestRun = run[0];
        longestRunDate = run[1];
      }
    });
  
    return [longestRun, longestRunDate];
  }
  
  /**
   * Returns the entries from the given athlete's dedicated sheet.
   * 
   * @return a list of activity IDs
   */
  function getIDsFromAthleteSheet(athlete) {
    var athleteSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(athlete);
    if (athleteSheet == null) {
      Logger.log(`${athlete} does not have a sheet. Exiting getIDsFromAthleteSheet()...`);
      return -1;
    }
    return athleteSheet.getRange(2, 2, athleteSheet.getLastRow(), 1).getValues().filter((id) => id.toString().match("^[0-9]{10}$")).flat();
  }
  
  /**
   * Returns the given athlete's activities for the current week.
   * 
   * @return a list of activities
   */
  function getAthletesRunsFromThisWeek(sheet, athlete) {
    var datesWithinThisWeek = getDatesFromCurrentWeek();
  
    var startRow = 0;
    if (sheet.getSheetName() == "GOONS") startRow = START_ROW_OF_ACTIVITIES_GOONS_SHEET;
    else startRow = 2;
    var athleteActivities = sheet.getRange(startRow, 1, sheet.getLastRow(), getNumberOfHeaders(sheet, startRow - 1, 1)).getValues().filter(
      (activity) => datesWithinThisWeek.includes(formatDate(activity[6])) && activity.includes(athlete)
    );
  
    Logger.log(`${athlete} has ${athleteActivities.length} activities from this week... \n${JSON.stringify(athleteActivities, null, 2)}`);
    return athleteActivities;
  }
  
  /**
   * Divides the given time by the number of runs to get an average.
   *    Note: This is used for time average and pace average.
   * 
   * @return a time of the format hh:mm:ss.
   */
  function getDividedTime(talliedUnit, numRuns) {
    // Checking to see if we have an invalid date
    if (!(Object.prototype.toString.call(talliedUnit) === '[object Date]')) {
      Logger.log("The talliedUnit is NOT a valid Date.");
      return;
    }
  
    var h = talliedUnit.getHours(), m = talliedUnit.getMinutes(), s = talliedUnit.getSeconds();
  
    var talliedUnitInSeconds = (h*3600) + (m*60) + s;
    var secondsDivided = talliedUnitInSeconds / numRuns;
  
    h = Math.floor(secondsDivided / 3600);
    m = Math.floor((secondsDivided % 3600) / 60);
    s = Math.floor((secondsDivided % 3600) % 60);
  
    // Converting if the resulting time unit only has one digit (e.g. 1)
    if (h.toString().length == "1.0") h = `0${h}`;
    if (m.toString().length == "1.0") m = `0${m}`;
    if (s.toString().length == "1.0") s = `0${s}`;
  
    return (h + ":" + m + ":" + s); // 00:39:34
  }
  
  /**
   * Add two string time values (HH:mm:ss) with javascript
   * Source: https://gist.github.com/joseluisq/dc205abcc9733630639eaf43e267d63f
   * 
   * Usage:
   *  > addTimes('04:20:10', '21:15:10');
   *  > "25:35:20"
   *  > addTimes('04:35:10', '21:35:10');
   *  > "26:10:20"
   *  > addTimes('30:59', '17:10');
   *  > "48:09:00"
   *  > addTimes('19:30:00', '00:30:00');
   *  > "20:00:00"
   *
   * @param {String} startTime  String time format
   * @param {String} endTime  String time format
   * @returns {String}
   */
  function addTimes (startTime, endTime) {
    var times = [ 0, 0, 0 ]
    var max = times.length
  
    var a = (startTime || '').split(':')
    var b = (endTime || '').split(':')
  
    // normalize time values
    for (var i = 0; i < max; i++) {
      a[i] = isNaN(parseInt(a[i])) ? 0 : parseInt(a[i])
      b[i] = isNaN(parseInt(b[i])) ? 0 : parseInt(b[i])
    }
  
    // store time values
    for (var i = 0; i < max; i++) {
      times[i] = a[i] + b[i]
    }
  
    var hours = times[0]
    var minutes = times[1]
    var seconds = times[2]
  
    if (seconds >= 60) {
      var m = (seconds / 60) << 0
      minutes += m
      seconds -= 60 * m
    }
  
    if (minutes >= 60) {
      var h = (minutes / 60) << 0
      hours += h
      minutes -= 60 * h
    }
  
    return ('0' + hours).slice(-2) + ':' + ('0' + minutes).slice(-2) + ':' + ('0' + seconds).slice(-2)
  }
  
  /**
   * Parses the duration into hh:mm:ss (the actual correct way).
   */
  function parseDuration(duration) {
    var durationHours = duration.getHours();
    if (duration.getHours().toString().length != "2.0") {
      durationHours = `0${durationHours}`;
    }
    var durationMinutes = duration.getMinutes(); 
    if (duration.getMinutes().toString().length != "2.0") {
      durationMinutes = `0${durationMinutes}`;
    }
    var durationSeconds = duration.getSeconds(); 
    if (duration.getSeconds().toString().length != "2.0") {
      durationSeconds = `0${durationSeconds}`;
    }
    return (`${durationHours}:${durationMinutes}:${durationSeconds}`);
  }
  
  /**
   * Formats the date in the format of MM/dd/yyyy.
   *    Example: 3/3/23 (March 3, 2023)
   * 
   * @return a formatted date
   */
  function formatDate(date) {
    return Utilities.formatDate(new Date(date), "America/New_York", "MM/dd/yyyy");
  }
  
  /**
   * Gets the Dates from the current week (in the "GOONS" sheet) that have occurred thus far,
   *    where Monday marks the beginning of the week and Sunday marks the end. 
   * 
   * @return a list of Dates
   */
  function getDatesFromCurrentWeek() {
    // Janky line to use momentjs, not sure how to do it otherwise (couldn't find a script ID)
    eval(UrlFetchApp.fetch('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js').getContentText());
    
    // Acquiring the dates that mark the start and end of the current week
    var currentDate = moment();
    var weekStart = formatDate(currentDate.clone().startOf('isoWeek'));
    var weekEnd = formatDate(currentDate.clone().endOf('isoWeek'));
  
    var datesFromSheet = getUniqueDatesFromGoonsSheet(); // Acquiring the dates from the "GOONS" sheet
  
    // Filtering down to dates that have occurred thus far in the current week
    return datesFromSheet.filter((date) => (date <= weekEnd) && (date >= weekStart));
  }
  
  /**
   * Gets the Date of the start of the week (where Monday is the start) in the format of MM/dd/yyyy.
   *    Example Date: 03/17/2023
   * 
   * @return a parsed date
   */
  function getStartOfWeek() {
    eval(UrlFetchApp.fetch('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js').getContentText());
    return formatDate(moment().clone().startOf('isoWeek'));
  }
  
  /**
   * Gets the Date of the end of the week (where Sunday is the end) in the format of MM/dd/yyyy.
   *    Example Date: 03/17/2023
   * 
   * @return a parsed date
   */
  function getEndOfWeek() {
    eval(UrlFetchApp.fetch('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js').getContentText());
    return formatDate(moment().clone().endOf('isoWeek'));
  }
  
  /**
   * Determines if today is the last day of the week (in this case Sunday).
   * 
   * @return true if it's Sunday, or false otherwise.
   */
  function isLastDayOfWeek() {
    eval(UrlFetchApp.fetch('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js').getContentText());
    return (formatDate(moment()) == getEndOfWeek());
  }
  
  /**
   * Gets the full Date (e.g. 03/02/2023) from X days ago, where X is any positive integer.
   * 
   * @return a parsed date
   */
  function getXDaysAgo(daysAgo) {
    var date = new Date(Date.now()); // Example: Thu Mar 02 2023 20:32:20 GMT-0500 (Eastern Standard Time)
  
    var currentMilliseconds = new Date().getTime();
    var xDaysAgoMilliseconds = currentMilliseconds - (86400000 * daysAgo); // 86,400,000 milliseconds per 1 day
  
    var fullDateXDaysAgo = formatDate(xDaysAgoMilliseconds);
    return new Date(fullDateXDaysAgo);
  }
  
  /**
   * Gets a list of unique date entries from the "GOONS" sheet.
   * 
   * @return a parsed date (e.g. "03/20/2023")
   */
  function getUniqueDatesFromGoonsSheet() {
    var goonsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS");
    var dates = goonsSheet.getRange(START_ROW_OF_ACTIVITIES_GOONS_SHEET, 7, goonsSheet.getLastRow(), 1).getValues().flat().filter((date) => date);
    var formattedDates = [];
  
    dates.forEach((date) => {
      var formattedDate = formatDate(date);
      if (!formattedDates.includes(formattedDate)) formattedDates.push(formattedDate);
    });
  
    return formattedDates;
  }
  
  /**
   * Returns a unique list of athletes based on the "GOONS" sheet.
   * 
   * @param sheet, the sheet to acquire the athletes list from
   * @return uniqueAthletesList, a list of unique athletes
   */
  function getListOfUniqueAthletes(sheet) {
    // Acquiring the current list of athletes from the spreadsheet and filtering out empty values
    var currAthletesList = sheet.getRange(START_ROW_OF_ACTIVITIES_GOONS_SHEET, 1, sheet.getLastRow(), 1).getValues().flat().filter((athlete) => athlete && ATHLETE_NAMES.includes(athlete));
    var uniqueAthletesList = [];
    
    currAthletesList.forEach(
      function(athlete) {
        if (!uniqueAthletesList.includes(athlete)) {
          uniqueAthletesList.push(athlete);
        }
      }
    );
  
    return uniqueAthletesList;
  }
  
  /**
   * Returns the names of all sheets.
   * 
   * @return a list of sheet names
   */
  function getAllSheets() {
    // Acquiring sheets
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheets = ss.getSheets();
    var sheetNames = [];
  
    // Iterating through sheets and adding to array
    sheets.forEach(
      function (sheet) {
        sheetNames.push(sheet.getName());
      }
    );
  
    return sheetNames;
  }
  
  /**
   * Returns the names of the athlete sheets.
   * 
   * @return a list of sheet names
   */
  function getAthleteSheets() {
    var nonAthleteSheets = ["TO DO / THOUGHTS", "GOONS", "GOONS RECAP"];
    return getAllSheets().filter((sheet) => !nonAthleteSheets.includes(sheet));
  }