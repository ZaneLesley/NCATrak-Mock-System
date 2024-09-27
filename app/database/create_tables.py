import psycopg2
from config import load_config

def create_table():

    command = (
        """
        CREATE TABLE personal_profile (
            first_name VARCHAR(255) NOT NULL,
            middle_initial VARCHAR(255),
            last_name VARCHAR(255) NOT NULL,
            nickname VARCHAR(255),
            birthdate DATE NOT NULL,
            ssn VARCHAR(255) PRIMARY KEY,
            bio_gender VARCHAR(255),
            religion VARCHAR(255),
            race VARCHAR(255),
            language VARCHAR (255),
            voca_classifications VARCHAR(255),
            comments VARCHAR(255),
            prior_convictions BOOL,
            convicted_against_children BOOL,
            sexual_offender BOOL,
            sexual_predator BOOL
        )
        """
    )

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    create_table()