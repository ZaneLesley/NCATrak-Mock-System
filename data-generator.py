"""
An Example on how data generation works. Also Using this to test the Requirements.txt file.
and installation of everything.
"""

from faker import Faker
import pandas as pd
from rich import print

def generate_data(n):
    data = []
    fake = Faker()
    Faker.seed(0)
    for i in range (n):
        person = {}
        person['cust_id'] = fake.unique.random_int(min = 0, max=9999)
        if fake.random_int(min = 0, max = 1) == 0:
            person['first_name'] = fake.first_name_male()
            person['second_name'] = fake.first_name_male()
            person['last_name'] = fake.last_name()
            person['sex'] = "male"
        else:
            person['first_name'] = fake.first_name_female()
            person['second_name'] = fake.first_name_female()
            person['last_name'] = fake.last_name()
            person['sex'] = "female"
        person['date_of_birth'] = fake.date_of_birth(minimum_age = 18, maximum_age = 100)
        person['address'] = fake.address()
        person['acct_no'] = fake.unique.random_int(min= 0, max= 100000)
        person['acct_bal'] = fake.pydecimal(right_digits = 2, positive = True, min_value = 1, max_value = 10000)
        person['acct_type'] = fake.random_int(min = 0, max = 1000, step = 100)
        person['acct_opening_date'] = fake.date_of_birth(minimum_age = 0, maximum_age = 25)
        data.append(person)
    return pd.DataFrame(data)


if __name__ == "__main__":
    print("[bold blue]NCA-Trak-Mock Data Generator")
    print("[yellow]How many data entries would you like to be generated?")
    n = int(input())
    print("[yellow]Generating Data...")
    final_data = generate_data(n)
    print("[yellow]Writing .csv file...")
    final_data.to_csv('data.csv')
    print("[green]Data written to /data.csv")