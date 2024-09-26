import psycopg2
from config import load_config

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
    
    tables_file = open("app/database/tables_master_list.txt", "r")
    table_name = tables_file.readline().strip()
    
    while (len(table_name) != 0):
        print(f"Creating new table {table_name}")
        sql_file_name = f"app/database/data_tables/{table_name}_table.sql"
        sql_file = open(sql_file_name, "r")
        commands = sql_file.read().split(";")
        for command in commands:
            if not command == "":
                execute_command(command)
        sql_file.close()
        table_name = tables_file.readline().strip()
    tables_file.close()

    print("All database tables created. Databases will need to be repopulated using generated data.")
