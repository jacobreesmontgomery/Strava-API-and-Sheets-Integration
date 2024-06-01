import os
import base64
import json
from email.mime.text import MIMEText
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import schedule
import time
from dotenv import load_dotenv
import csv

# Loading environment variables from the .env file
load_dotenv()
ATHLETE_NAMES_PARALLEL_ARR = json.loads(os.getenv("ATHLETE_NAMES_PARALLEL_ARR"))
ATHLETE_EMAILS_PARALLEL_ARR = json.loads(os.getenv("ATHLETE_EMAILS_PARALLEL_ARR"))
ATHLETE_NICKNAMES_PARALLEL_ARR = json.loads(os.getenv("ATHLETE_NICKNAMES_PARALLEL_ARR")) 
ATHLETE_DATA_FIELDNAMES = json.loads(os.getenv("ATHLETE_DATA_FIELDNAMES"))
RECAP_FIELDNAMES = json.loads(os.getenv("RECAP_FIELDNAMES"))

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def establish_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}.")
                creds = None
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'python\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_email(subject, body, to):
    service = establish_creds()
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {
        'raw': raw
    }

    try:
        message = (service.users().messages().send(userId=ATHLETE_EMAILS_PARALLEL_ARR[0], body=message)
            .execute())
        print(f'Message Id: {message["id"]}')
    except Exception as e:
        print(f'An error occurred while sending the email: {e}')

def read_csv(file_path, fieldnames, athlete):
    """
        Read all rows from a CSV file.
    """
    print(f"\nSTART of read_csv() w/ arg(s)...\n\tfile_path: {file_path}\n\tfieldnames: {fieldnames}\n\tathlete: {athlete}")
    runData = f"{fieldnames}\n"
    with open(file_path, mode='r', newline='') as file:
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist. Exiting read_csv()...")
        if os.stat(file_path).st_size == 0:
            print(f"The file {file_path} is empty. Exiting read_csv()...")
        
        reader = csv.DictReader(file, fieldnames=fieldnames, delimiter=',')
        if athlete:
            # We're getting recap data for the given athlete
            for row in reader:
                if row["ATHLETE"] == athlete:
                    runData += str(row)
                    break
        else:
            # We're getting the athlete's week of training
            next(reader) # Skipping the header
            for row in reader:
                runData += f"{row}\n"
    print(f"END of read_csv() w/ return(s)...\n\trunData: {runData}\n")
    return runData

def job():
    i = 0
    for athlete in ATHLETE_NAMES_PARALLEL_ARR:
        eachTrainingDay = read_csv(file_path=f"python\code\datasetup\data\weekly_stats\{athlete}_WEEK_STATS.csv", fieldnames=ATHLETE_DATA_FIELDNAMES, athlete="")
        recapOfWeek = read_csv(file_path=r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv", fieldnames=RECAP_FIELDNAMES, athlete=athlete.upper())
        send_email(
            subject='Weekly Recap',
            body=
            f"""
            Hey, {ATHLETE_NICKNAMES_PARALLEL_ARR[0]}!

            Here is a recap of your training week:
            {eachTrainingDay}

            Here is your week's final stats:
            {recapOfWeek}
            """,
            to=ATHLETE_EMAILS_PARALLEL_ARR[0]
        )
        i += 1
        break

job()

# Schedule the job to run every Monday at 9 PM
# schedule.every().sunday.at("21:00").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
