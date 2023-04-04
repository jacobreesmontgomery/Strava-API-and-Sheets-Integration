/**
 * This time-triggered function--run every day at 8-9PM--acquires 
 *    the week's recap data for each athlete and consolidates it all in one sheet, "GOONS RECAP."
 */
function generateGoonsRecapSheet() {
  // Initial check for the existence of all of the athlete sheets
  checkAthleteSheets();
  // Populate the sheet with the weekly recap data (basic stats and workout stats)
  populateGoonsRecapSheet(getWeekSummaries(), getWorkoutSummaries());
}

/**
 * Populates the "GOONS RECAP" sheet with the acquired data from getWeekSummaries().
 * 
 * @param summariesList, the list of weekly recap stats for each athlete
 * @param workoutSummariesList, the list of weekly workout recap stats for each athlete
 */
function populateGoonsRecapSheet(summariesList, workoutSummariesList) {
  var goonsRecapSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS RECAP");
  // Creating the sheet if it doesn't exist
  if (goonsRecapSheet == null) {
    Logger.log("The 'GOONS RECAP' sheet does not exist and will be created and formatted before proceeding...");
    goonsRecapSheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet();
    goonsRecapSheet.setName("GOONS RECAP");
  }
  goonsRecapSheet.getRange(1, 1, 1, 1).setValue(`This is the week of ${getStartOfWeek()}-${getEndOfWeek()}`).setFontWeight("bold");

  /* BASIC RECAP STATS */ 
  // Headers and borders
  goonsRecapSheet.getRange(3, 1, 1, summariesList[0].length).setBackground("lightgrey").setFontWeight("bold").setValues([RECAP_STATS_HEADERS_GOONS_RECAP]);
  goonsRecapSheet.getRange(3, 1, 1 + summariesList.length, summariesList[0].length).setBorder(true, true, true, true, true, true);

  // Column formatting
  goonsRecapSheet.getRange(4, 2, summariesList.length, 1).setNumberFormat("00.00");
  goonsRecapSheet.getRange(4, 3, summariesList.length, 1).setNumberFormat("hh:mm:ss");
  goonsRecapSheet.getRange(4, 4, summariesList.length, 1).setNumberFormat("0");
  goonsRecapSheet.getRange(4, 5, summariesList.length, 1).setNumberFormat("00.00");
  goonsRecapSheet.getRange(4, 6, summariesList.length, 1).setNumberFormat("hh:mm:ss");
  goonsRecapSheet.getRange(4, 7, summariesList.length, 1).setNumberFormat("hh:mm:ss");
  goonsRecapSheet.getRange(4, 8, summariesList.length, 1).setNumberFormat("00.00");
  goonsRecapSheet.getRange(4, 9, summariesList.length, 1).setNumberFormat("MM/dd/yyyy");

  // Adding the stat summaries to the sheet and sorting by tallied mileage
  goonsRecapSheet.getRange(4, 1, summariesList.length, summariesList[0].length).setValues(summariesList).sort({column: 2, ascending: false});

  /* WORKOUT RECAP STATS */ 
  // Headers and borders
  goonsRecapSheet.getRange(ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET + summariesList.length + ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_HEADER, 1, 1, workoutSummariesList[0].length).setBackground("lightgrey").setFontWeight("bold").setValues([WORKOUT_RECAP_STATS_GOONS_RECAP]);
  goonsRecapSheet.getRange(ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET + summariesList.length + ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_HEADER, 1, 1 + workoutSummariesList.length, workoutSummariesList[0].length).setBorder(true, true, true, true, true, true);

  // Column formatting
  goonsRecapSheet.getRange(ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET + summariesList.length + ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_STATS, 2, workoutSummariesList.length, 1).setNumberFormat("0");
  goonsRecapSheet.getRange(ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET + summariesList.length + ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_STATS, 6, workoutSummariesList.length, 1).setNumberFormat("MM/dd/yyyy");
  goonsRecapSheet.getRange(ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET + summariesList.length + ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_STATS, 8, workoutSummariesList.length, 1).setNumberFormat("hh:mm:ss AM/PM");

  // Adding the workout recap stats to the sheet by the same order as the weekly stat summaries
  goonsRecapSheet.getRange(ROW_OF_WEEKLY_RECAP_HEADER_RECAP_SHEET + summariesList.length + ROWS_DOWN_FROM_LAST_WEEKLY_RECAP_ROW_STATS, 1, workoutSummariesList.length, workoutSummariesList[0].length).setValues(workoutSummariesList).sort([{column: 1, ascending: false}, {column: 2, ascending: false}]);

  // Aligning ALL cells to be left-justified
  goonsRecapSheet.getRange(1, 1, goonsRecapSheet.getLastRow(), goonsRecapSheet.getLastColumn()).setHorizontalAlignment("left");
}

/**
 * Determines if any athlete sheets need to be created, and does so as necessary.
 */
function checkAthleteSheets() {
  var uniqueAthletesList = getListOfUniqueAthletes(SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS"));
  var existingAthleteSheets = getAllSheets().filter((sheet) => uniqueAthletesList.includes(sheet));
  if (existingAthleteSheets.length != NUM_OF_ACTIVE_GOONS) {
    Logger.log(`${NUM_OF_ACTIVE_GOONS - existingAthleteSheets.length} athlete's sheets are missing and must be created...`);
    createAthleteSheetsIfNotExists();
  }
}

/**
 * Gets each athlete's weekly recap data.
 * 
 * @return a list containing the workout summary data
 */
function getWeekSummaries() {
  var summaryList = [];

  // Iterating over each athlete's sheet to grab their data and add to a 2D array
  var uniqueAthletesList = getListOfUniqueAthletes(SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS"));
  getAllSheets().filter((sheet) => uniqueAthletesList.includes(sheet) && SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheet).getRange(2,1).getValue()).forEach((athleteSheetName) => {
    var athleteSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(athleteSheetName);
    // Acquire athlete's stats for the week and append their name to the front of the array
    var recapStats = athleteSheet.getRange(1 + getActivitiesFromAthleteSheet(athleteSheet).length + ROWS_DOWN_FROM_LAST_RUN_FOR_RECAP_STATS, 1, 1, NUM_OF_RECAP_STATS).getValues().flat(); // the - 1 is to account for the name addition
    recapStats.unshift(athleteSheetName);

    // Add the values (as a single array) to the 2D array, summaryList
    summaryList.push(recapStats);
  });

  return summaryList;
}

/**
 * Acquires the workout summary data from each athlete's sheet.
 * 
 * @return a list containing the workout summary data
 */
function getWorkoutSummaries() {
  var wktSummaryList = [];

  // Iterate over each athlete's sheet to grab their workout data and add to a 2D array
  getAllSheets().filter((sheet) => getListOfUniqueAthletes(SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS")).includes(sheet) && SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheet).getRange(2,1).getValue()).forEach((athleteSheetName) => {
    var athleteSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(athleteSheetName);
    var numWorkouts = getWorkoutStatsFromAthleteSheet(athleteSheet).length;
    var wktRecapStats = [];
    if (numWorkouts > 0)  {
      // Getting the workout values
      wktRecapStats = athleteSheet.getRange(1 + getActivitiesFromAthleteSheet(athleteSheet).length + ROWS_DOWN_FROM_LAST_RUN_FOR_WORKOUT_STATS, 1, numWorkouts, NUM_OF_WORKOUT_RECAP_STATS).getValues().flat();
      wktRecapStats.unshift(athleteSheetName);
      
      // Add the values (as a single array) to the 2D array, summaryList
      wktSummaryList.push(wktRecapStats);
    }
  });

  return wktSummaryList;
}

/**
 * This time-triggered function--run every Monday at 12AM-1AM--clears the "GOONS RECAP" sheet
 *    where necessary to get it ready to go for the next population.
 */
function clearGoonsRecapSheet() {
  var recapSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("GOONS RECAP");

  // Clearing out ALL content from the sheet
  recapSheet.getRange(1, 1, recapSheet.getLastRow(), recapSheet.getMaxColumns()).clearContent().clearFormat();
}

