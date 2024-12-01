import psycopg2
import os
from rich import print
from database.create_tables import main as create_tables
from generator.data_generator import main as data_generator
from database.populate_database import main as populate_database

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
    
while True:
    n = input()
    if not (n.isdigit() and 4 >= int(n) > 0):
        print("[red]Please insert a number from the options listed.")
    else:
        break
n = int(n)

# TODO: Implement Each one
# Complete Install
if n == 1:
    cwd = os.path.dirname(os.path.abspath(__file__))
    database_ini_path = os.path.join(cwd, "database", "database.ini")
    with open(database_ini_path, "w") as file:
        file.write("[postgresql]\n")
        data = [input("[yellow]Enter the host\n"), input("[yellow]Enter the database name\n"), input("[yellow]Enter user name\n"),
                input("[yellow]Enter password\n")]
        file.write(f"host={data[0]}\ndatabase={data[1]}\nuser={data[2]}\npassword={data[3]}")
    print("[green]Database.ini file has been created.")

    create_tables()
    print("[green]Database tables created.")
    data_generator()
    print("[green]Database tables generated.")
    populate_database()
    print("[green]Database tables populated.")
    print("[green][bold] Installation complete.")

# Data Regeneration
elif n == 2:
    pass
# Configure Data Generation Defaults
elif n == 3:
    pass
# Delete Database
elif n == 4:
    pass
        
    