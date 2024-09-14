import psycopg2
from config import load_config

def insert_personal_profile():

    insert_query =  (
        """
        INSERT INTO test_setup_database(first_name, 
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
        sexual_predator)"
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    )

    data_file = open("data.csv")
    print(data_file.readline())
    data_file.close()


if __name__ == '__main__':
    insert_personal_profile()