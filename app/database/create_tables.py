import psycopg2
from config import load_config

tables_to_create = [
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

def execute_command(command):

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':

    # Delete all existing tables so the new database can be built
    print("Deleting old database tables...")
    delete_tables_file = open("app/database/delete_tables.sql", "r")
    commands = delete_tables_file.read().split(";")
    for command in commands:
        if not command == "":
            execute_command(command)
    delete_tables_file.close()
    
    for table_name in tables_to_create:
        print(f"Creating new table {table_name}")
        sql_file_name = f"app/database/data_tables/{table_name}_table.sql"
        sql_file = open(sql_file_name, "r")
        commands = sql_file.read().split(";")
        for command in commands:
            if not command == "":
                execute_command(command)
        sql_file.close()

    print("All database tables created. Databases will need to be repopulated using generated data.")
