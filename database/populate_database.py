import os
from config import load_config
from connect import connect
import csv

def insert_personal_profile():

    insert_query = """
    INSERT INTO personal_profile (
        first_name, 
        middle_initial, 
        last_name, 
        nickname, 
        birthdate, 
        ssn, 
        bio_gender, 
        religion, 
        race, 
        language, 
        voca_classifications, 
        comments, 
        prior_convictions, 
        convicted_against_children, 
        sexual_offender, 
        sexual_predator
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
        
    config = load_config()
    conn = connect(config)
    if conn is None:
        print("Failed to connect to the database")
        return
    
    file_path = os.path.join("..", "data.csv")
    with open(file_path, 'r') as data:
        parser = csv.reader(data)
        next(parser)
        
        with conn.cursor() as cur:
            for row in parser:
                cur.execute(insert_query, row)
            
            conn.commit()

if __name__ == '__main__':
    insert_personal_profile()