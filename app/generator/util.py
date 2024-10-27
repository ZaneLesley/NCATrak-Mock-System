from datetime import datetime, timedelta
import random
import os
from rich import print
import pandas as pd

# Function to generate random start and end times within the range
def generate_meeting_times():
    day_start = datetime.strptime("08:00", "%H:%M")
    day_end = datetime.strptime("20:00", "%H:%M")

    # Generate start_time within the range of 8:00 AM to 7:00 PM (so there's at least 1 hour for the meeting)
    start_time = day_start + timedelta(minutes=random.randint(0, (day_end - day_start).seconds // 60 - 60))

    max_end_time = min(day_end, start_time + timedelta(minutes=60))  # Cap end_time to be within 8:00 PM
    end_time = start_time + timedelta(minutes=random.randint(1, (max_end_time - start_time).seconds // 60))

    start_time_str = start_time.strftime("%H:%M")
    end_time_str = end_time.strftime("%H:%M")
    return start_time_str, end_time_str

def find_column(key: str, column: str, table: list, value: str) -> dict:
    for item in table:
        if item[column] == key:
            return item[value]
    return None

def write_to_csv(data: list, name: str):
    df = pd.DataFrame(data)
    
    folder = "csvs"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, name + ".csv")
    
    df.to_csv(filename, index=False)    
    print(f"[green]Successfully wrote data to {filename}.")
    