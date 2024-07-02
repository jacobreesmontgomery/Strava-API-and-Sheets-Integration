from datetime import timedelta
import csv
from dotenv import load_dotenv
import os
import json


load_dotenv()
RECAP_FIELDNAMES = json.loads(os.getenv("RECAP_FIELDNAMES"))


def get_index_of_key(dictionary, key_to_find):
    """
        TODO: Add description.
    """
    print(f"START of get_index_of_key() w/ arg(s)...\n\tdictionary: {dictionary}\n\tkey_to_find: {key_to_find}")
    index = 0
    for key in dictionary:
        if int(key) == int(key_to_find):
            print(f"END of get_index_of_key() w/ return(s)...\n\tindex: {index}\n")
            return index
        index += 1
    print(f"END of get_index_of_key() w/ return(s)...\n\tindex: -1\n")
    return -1  # Key not found in the dictionary


def format_seconds(seconds):
    """
        Formats seconds to the format of HH:MM:SS.
    """
    print(f"\nSTART of format_seconds() w/ arg(s)...\n\tseconds: {seconds}")
    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format as HH:MM:SS
    print(f"\nEND of format_seconds() w/ return(s)...\n\t{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}\n")
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def calculate_pace(total_seconds, distance_miles):
    """
        Calculates pace (MM:SS) using the total seconds and
        distance of the run (mi). 
    """
    print(f"\nSTART of calculate_pace() w/ arg(s)...\n\ttotal_seconds: {total_seconds}\n\tdistance_miles: {distance_miles}")
    # Convert total seconds to minutes
    total_minutes = total_seconds / 60
    
    # Calculate pace in minutes per mile
    pace_minutes_per_mile = total_minutes / distance_miles
    
    # Convert pace to MM:SS format
    pace_seconds = int(pace_minutes_per_mile * 60)
    minutes, seconds = divmod(pace_seconds, 60)
    
    print(f"\nEND of calculate_pace() w/ return(s)...\n\t{minutes:02d}:{seconds:02d}\n")
    return f"{minutes:02d}:{seconds:02d}"


def format_to_hhmmss(time_str):
    """
        Format a string to HH:MM:SS.
    """
    print(f"\nSTART of format_to_hhmmss() w/ arg(s)...\n\ttime_str: {time_str}")
    # Split the time string by colon
    parts = time_str.split(':')
    
    if len(parts) != 3:
        raise ValueError(f"Incorrect time format: {time_str}")
    
    # Pad each part with leading zeros to ensure two digits
    hours = parts[0].zfill(2)
    minutes = parts[1].zfill(2)
    seconds = parts[2].zfill(2)
    
    # Join the parts back together with colons
    formatted_time = f"{hours}:{minutes}:{seconds}"
    print(f"END of format_to_hhmmss() w/ return(s)...\n\tformatted_time: {formatted_time}\n")
    return formatted_time


def time_str_to_seconds(time_str):
    """

    """
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds


def divide_time_by_number(time_str, divisor):
    """

    """
    total_seconds = time_str_to_seconds(time_str)
    divided_seconds = total_seconds / divisor
    return divided_seconds


def seconds_to_time_str(total_seconds):
    """

    """
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds % 3600) / 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def divide_time_str_by_number(time_str, divisor):
    """

    """
    total_seconds = time_str_to_seconds(time_str)
    divided_seconds = total_seconds / divisor
    return seconds_to_time_str(divided_seconds)


def tally_time(run_times):
    """
        Tallies up all of the incoming run's times.
    """   
    print(f"\nSTART of tally_time() w/ argument(s): \n\trun_times: {run_times}") 
    total_duration = timedelta(hours=0, minutes=0, seconds=0)
    for time in run_times:
        time = format_to_hhmmss(time_str=time)
        if len(time) != 8 or time[2] != ':' or time[5] != ':':
            raise ValueError(f"Incorrect time format: {time}")
        total_duration = total_duration + timedelta(hours=int(time[:2]), minutes=int(time[3:5]), seconds=int(time[6:]))
    print(f"END of tally_time() w/ return(s)... \n\ttotal_duration: {total_duration}\n\tstr(total_duration): {str(total_duration)}\n")
    return total_duration, str(total_duration)


def read_csv(file_path):
    """
        Read all rows from a CSV file.
    """
    print(f"\nSTART of read_csv() w/ arg(s)...\n\tfile_path: {file_path}")
    rows = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file, fieldnames=RECAP_FIELDNAMES, delimiter=',')
        rows = list(reader)
    print(f"END of read_csv() w/ return(s)...\n\trows: {rows}\n")
    return rows