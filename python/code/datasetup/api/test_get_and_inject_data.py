import unittest
from GetAndInjectData import parse_description
import os
from dotenv import load_dotenv
import json
import sys

# Loading environment variables from the .env file
load_dotenv()

# VARIABLES
ACTIVITIES_FILE_NAME = "ATHLETE_DATA"
ATHLETE_DATA_FIELDNAMES = json.loads(os.getenv("ATHLETE_DATA_FIELDNAMES"))
athlete_data_file = "C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code/datasetup/data/main_data/ATHLETE_DATA.csv"
OPTIONAL_FIELDS = os.getenv("OPTIONAL_FIELDS")

# TODO: Figure out how TF to do this.

class TestParseDescription(unittest.TestCase):

    def test_parse_description_with_different_field_order(self):
        description = "POWER:135|RATING:8|RPE:3. Good run! No issues."
        rpe, rating, avgPower = parse_description(description)
        self.assertEqual(rpe, 3, "RPE value is incorrect.")
        self.assertEqual(rating, 8, "Rating value is incorrect.")
        self.assertEqual(avgPower, 135, "Average power value is incorrect.")

    def test_parse_description_with_extra_spaces(self):
        description = "  POWER:135  |  RATING:8  |  RPE:3. Good run! No issues.  "
        rpe, rating, avgPower = parse_description(description)
        self.assertEqual(rpe, 3, "RPE value is incorrect.")
        self.assertEqual(rating, 8, "Rating value is incorrect.")
        self.assertEqual(avgPower, 135, "Average power value is incorrect.")

    def test_parse_description_with_mixed_case_field_names(self):
        description = "pOwEr:135|rAtInG:8|RpE:3. Good run! No issues."
        rpe, rating, avgPower = parse_description(description)
        self.assertEqual(rpe, 3, "RPE value is incorrect.")
        self.assertEqual(rating, 8, "Rating value is incorrect.")
        self.assertEqual(avgPower, 135, "Average power value is incorrect.")

    def test_parse_description_with_multiple_spaces_between_fields(self):
        description = "POWER:135  |  RATING:8  |  RPE:3  .  Good run! No issues."
        rpe, rating, avgPower = parse_description(description)
        self.assertEqual(rpe, 3, "RPE value is incorrect.")
        self.assertEqual(rating, 8, "Rating value is incorrect.")
        self.assertEqual(avgPower, 135, "Average power value is incorrect.")

    def test_parse_description_with_no_spaces_around_colon(self):
        description = "POWER:135|RATING:8|RPE:3.Good run!No issues."
        rpe, rating, avgPower = parse_description(description)
        self.assertEqual(rpe, 3, "RPE value is incorrect.")
        self.assertEqual(rating, 8, "Rating value is incorrect.")
        self.assertEqual(avgPower, 135, "Average power value is incorrect.")

if __name__ == '__main__':
    unittest.main()