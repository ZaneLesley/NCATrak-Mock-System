from datetime import datetime, timedelta
import random
import os
from rich import print
import pandas as pd

def generate_meeting_times(start_datetime: datetime):
    meeting_duration = timedelta(hours=random.randint(1, 4))
    end_datetime = start_datetime + meeting_duration
    end_timestamp = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return end_timestamp

def find_column(key: str, column: str, table: list, value: str):
    """
    Searches for a record in a table where the specified column matches the key
    and returns the value from another specified column.

    Args:
        key (str): The value to search for in the specified column.
        column (str): The column name to search within each record.
        table (list): The list of records (dictionaries) to search through.
        value (str): The column name whose value should be returned.

    Returns:
        The value from the specified column if a match is found; otherwise, an empty string.
    """
    for item in table:
        if item.get(column) == key:
            return item.get(value, '')
    return ''

def write_to_csv(data: list, name: str):
    """
    Writes a list of dictionaries to a CSV file, replacing any None or NaN values with empty strings.

    Args:
        data (list): The list of dictionaries containing data to be written to the CSV.
        name (str): The name of the CSV file (without the .csv extension).

    Returns:
        None
    """
    df = pd.DataFrame(data)
    
    # Replace any remaining None or NaN values with empty strings to maintain data type consistency
    df = df.where(pd.notnull(df), '')
    
    folder = "csvs"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, name + ".csv")
    
    df.to_csv(filename, index=False)    
    print(f"[green]Successfully wrote data to {filename}.")

