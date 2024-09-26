from faker import Faker
import pandas as pd
import random
from rich import print

# Religions
religions = ["Christianity", "Islam", "Hinduism", "Buddhism", "Other"]

# Races or Ethnicities
races = [
    "White",
    "Black or African American",
    "Asian",
    "Hispanic or Latino",
    "Native American",
    "Pacific Islander",
    "Middle Eastern",
    "Mixed Race",
    "Other",
]

def generate_data(n) -> pd.DataFrame:
    data = []
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(n):
        person = {}
        
        # Generates a male or female randomly.
        x = 0 if fake.random_int(min=0, max=1) == 0 else 1
        person["first_name"] = fake.first_name_male() if x == 0 else fake.first_name_female()
        person["middle_initial"] = fake.first_name_male()[0]  # Middle Initial
        person["last_name"] = fake.last_name_male() if x == 0 else fake.last_name_female()
        person["nickname"] = "placeholder"
        person["birthdate"] = fake.date_of_birth(minimum_age=18, maximum_age=100).strftime('%Y-%m-%d')
        person["ssn"] = fake.unique.ssn()
        person["bio_gender"] = "male" if x == 0 else "female"
        person["religion"] = random.choice(religions)
        person["race"] = random.choice(races)
        person["language"] = fake.language_name()
        person["voca_classifications"] = fake.random_uppercase_letter()
        person["comments"] = fake.sentence(nb_words=fake.random_int(min=0, max=15))
        person["prior_convictions"] = fake.boolean()
        person["convicted_against_children"] = fake.boolean()
        person["sexual_offender"] = fake.boolean()
        person["sexual_predator"] = fake.boolean()

        data.append(person)
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("[bold blue]NCA-Trak-Mock Data Generator")
    print("[yellow]How many data entries would you like to be generated?")
    n = int(input())
    print("[yellow]Generating Data...")
    final_data = generate_data(n)
    print("[yellow]Writing .csv file...")
    final_data.to_csv("data.csv", index=False)
    print("[green]Data written to /data.csv")
