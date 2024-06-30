import os
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import schedule
import time
from dotenv import load_dotenv
import csv
from jinja2 import Environment, FileSystemLoader
import requests
import random

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
    token_path = 'token.json'
    
    if os.path.exists(token_path):
        try:
            with open(token_path, 'r') as token_file:
                if os.stat(token_path).st_size != 0:
                    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                else:
                    print(f"Warning: {token_path} is empty. Generating a new token.")
        except json.JSONDecodeError:
            print(f"Error: {token_path} contains invalid JSON. Generating a new token.")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}.")
                creds = None
        else:
            flow = InstalledAppFlow.from_client_secrets_file('python\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
    
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_email(subject, body_html, to):
    service = establish_creds()
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['subject'] = subject

    # Attach the HTML message to the email
    part = MIMEText(body_html, 'html')
    message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {
        'raw': raw
    }

    try:
        message = (service.users().messages().send(userId='me', body=message)
            .execute())
        print(f'Message Id: {message["id"]}')
    except Exception as e:
        print(f'An error occurred while sending the email: {e}')

def read_csv(file_path, fieldnames, athlete, columns_to_include=None):
    print(f"\nSTART of read_csv() w/ arg(s)...\n\tfile_path: {file_path}\n\tfieldnames: {fieldnames}\n\tathlete: {athlete}\n\tcolumns_to_include: {columns_to_include}")
    runData = []
    with open(file_path, mode='r', newline='') as file:
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist. Exiting read_csv()...")
            return runData
        if os.stat(file_path).st_size == 0:
            print(f"The file {file_path} is empty. Exiting read_csv()...")
            return runData
        
        reader = csv.DictReader(file, fieldnames=fieldnames, delimiter=',')
        if athlete:
            # Looking at recap sheet to find athlete's row
            for row in reader:
                if row["ATHLETE"] == athlete:
                    if columns_to_include:
                        filtered_row = {col: row[col] for col in columns_to_include}
                        runData.append(filtered_row)
                    else:
                        # If nothing is passed, default to whole row
                        runData.append(row)
        else:
            # Looking at athlete's data sheet
            next(reader)  # Skipping the header
            for row in reader:
                if columns_to_include:
                    filtered_row = {col: row[col] for col in columns_to_include}
                    runData.append(filtered_row)
                else:
                    # If nothing is passed, default to whole row
                    runData.append(row)
    print(f"END of read_csv() w/ return(s)...\n\trunData: {runData}\n")
    return runData

def get_inspirational_quote():
    url = "https://type.fit/api/quotes"
    response = requests.get(url)
    if response.status_code == 200:
        quotes = response.json()
        # Filter inspirational quotes if needed, or pick a random one
        quote = random.choice(quotes)
        return f'"{quote["text"]}" - {quote.get("author")}'
    else:
        return "Quote not available at the moment."

def job():
    """
        Drives the main logic, including sending the emails to each athlete.
    """
    columns_to_include_weekly =["FULL DATE", "TIME", "MOVING TIME", "DISTANCE (MI)", "PACE (MIN/MI)", "SPM AVG", "HR AVG", "DESCRIPTION", "TOTAL ELEV GAIN (FT)"]
    columns_to_include_recap = ["TALLIED MILEAGE", "TALLIED TIME", "# OF RUNS", "MILEAGE AVG", "TIME AVG", "PACE AVG", "LONGEST RUN", "LONGEST RUN DATE"]
    # i = 0 # for testing purposes
    for athlete in ATHLETE_NAMES_PARALLEL_ARR:
        eachTrainingDay = read_csv(file_path=f"python\code\datasetup\data\weekly_stats\{athlete}_WEEK_STATS.csv", fieldnames=ATHLETE_DATA_FIELDNAMES, athlete="", columns_to_include=columns_to_include_weekly)
        recapOfWeek = read_csv(file_path=r"python\code\datasetup\data\recap\ATHLETE_WEEK_RECAP.csv", fieldnames=RECAP_FIELDNAMES, athlete=athlete.upper(), columns_to_include=columns_to_include_recap)
        
        print(f"eachTrainingDay: \n\t{eachTrainingDay}\nrecapOfWeek: \n\t{recapOfWeek}")

        # Load the template
        env = Environment(loader=FileSystemLoader(r'python\code\datasetup\templates'))
        template = env.get_template('email_template.html')
        
        # Render the template with context
        body = template.render(
            athlete_name=ATHLETE_NICKNAMES_PARALLEL_ARR[0], 
            eachTrainingDay=eachTrainingDay, 
            recapOfWeek=recapOfWeek,
            quote=get_inspirational_quote()
        )

        send_email(
            subject='Weekly Recap',
            body_html=body,
            to=ATHLETE_EMAILS_PARALLEL_ARR[0]
        )
        # i += 1 # for testing purposes (to only email myself)
        # break

# job() # for testing purposes

# Schedule the job to run every Sunday at 8 PM
schedule.every().sunday.at("20:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
