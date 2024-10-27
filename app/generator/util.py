from datetime import datetime, timedelta
import random
import os
from rich import print
import pandas as pd

# Function to generate random start and end times within the range
def generate_meeting_times(start_datetime: datetime):
    meeting_duration = timedelta(hours=random.randint(1, 4))
    end_datetime = start_datetime + meeting_duration
    return start_datetime, end_datetime

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
    