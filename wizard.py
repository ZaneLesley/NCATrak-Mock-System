import psycopg2
from rich import print
from app.database.config import load_config

db_tables = [
    "state",
    "child_advocacy_center",
    "cac_agency",
    "employee",
    "employee_account",
    "person",
    "cac_case",
    "case_person",
    "case_va_session",
    "case_va_session_attendee",
    "case_va_session_service",
    "case_mh_session",
    "case_mh_session_attendee",
    "case_mh_session_attribute_group",
    "case_mh_assessment_instrument",
    "case_mh_assessment",
    "case_mh_assessment_measure_scores",
    "case_mh_assessment_diagnosis",
    "case_mh_treatment_model",
    "case_mh_treatment_plan",
    "case_mh_provider",
    "case_mh_service_barriers"
]

def execute_db_command(command: str):

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == "__main__":
    print('''
[bold blue]WELCOME TO THE NCA-TRAK SETUP WIZARD\n
If you haven't yet, please read the [red]README.MD [blue]file in the home directory.
[bold red]IT IS VITAL YOU HAVE THE REQUIREMENTS INSTALLED BEFORE PROCEEDING

[yellow]Please Select From the following options:
[white]
[1] Complete Install
[2] Data Regeneration
[3] Configure Data Generation Defaults
[4] Delete Database
''')
    
while(True):
    n = input()
    if not (n.isdigit() and int(n) <= 4 and int(n) > 0):
        print("[red]Please insert a number from the options listed.")
    else:
        break
n = int(n)

# TODO: Implement Each one
# Complete Install
if n == 1:
    print("Creating database tables...")
    for table_name in db_tables:
        print(f"Creating new table {table_name}")
        sql_file_name = f"app/database/data_tables/{table_name}_table.sql"
        sql_file = open(sql_file_name, "r")
        commands = sql_file.read().split(";")
        for command in commands:
            if not command == "":
                execute_db_command(command)
        sql_file.close()
    
    print("Database tables created. Installation complete.")

# Data Regeneration
elif n == 2:
    pass
# Configure Data Generation Defaults
elif n == 3:
    pass
# Delete Database
elif n == 4:
    print("Are you sure you want to delete all tables in the database? This will delete any data you may have input or otherwise modified.")
    proceed = input("Enter [y/n]: ")
    while not (proceed.lower() == "y" or proceed.lower() == "n"):
        proceed = input("Enter [y/n]: ")
    if proceed.lower() == "y":
        print("Deleting data tables...")
        delete_tables_file = open("app/database/delete_tables.sql", "r")
        actions = delete_tables_file.read().strip().split(";")
        for action in actions:
            if not action == "":
                execute_db_command(action)
    