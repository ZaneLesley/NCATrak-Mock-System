import csv

# Path to the CSV file
file_path = 'data.csv'

with open(file_path, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if len(row) != 16:  # Adjust '16' to match the number of expected fields
            print(f"Line {i + 1} has {len(row)} fields")


