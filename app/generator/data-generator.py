from faker import Faker
from faker_education import SchoolProvider
import random
from datetime import datetime
from rich import print
import util

# Configurable
# Note: CAC_TO_GENERATE * CAC_TO_AGENCY_RATIO < 32767
#TODO: Write a check for this
CAC_TO_GENERATE = 5
CAC_TO_AGENCY_RATIO = 5         # Agency per CAC

# This is the age that I cutoff for prior_convictions, 
# convicted_against_children, sexual_offender and sexual_predator
PERSON_AGE_CUTOFF = 15


# Data Tables table name + data = variable name, refer to .xlsx for tables
#FIXME: fix some of the table names here
cac_data = []
agency_data = []
person_data = []
case_person_data = []
cac_case_data = []
case_va_session_attendee_data = []
case_va_session_log_data = []
case_va_session_service_data = []
case_mh_assessments_data = []
case_mh_assessment_instruments_data = []
case_mh_assessment_measure_scores_data = []
case_mh_diagonosis_log_data = []
case_mh_session_log_enc_data = []
case_mh_treatment_plans_data = []
case_mh_session_attendee_data = []
case_mh_attribute_group_data = []
case_mh_provider_log_data = []
case_mh_service_barriers_data = []
case_mh_treatment_models_data = []
state_data = []
employee_data = []
employee_account_data = []

# Custom Fields
religions = ["Christianity", "Islam", "Hinduism", "Buddhism", "Other"]

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

state_abbreviations = [
"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
"HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
"NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
"SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# (id, name)
assessment_instrument = [
(0, "Alabama Parenting Questionnaire", "Corporal Punishment"),
(1, "Alabama Parenting Questionnaire",	"Inconsistent Discipline"),
(2, "Alabama Parenting Questionnaire",	"Poor Monitoring/Supervision"),
(3, "Alabama Parenting Questionnaire",	"Positive Parenting"),
(4, "Brief Child Abuse Potential Inventory", "Abuse Risk"),
(5, "Brief Child Abuse Potential Inventory", "Family Conflict"),
(6, "Brief Child Abuse Potential Inventory", "Lie"),
(7, "Brief Child Abuse Potential Inventory", "Random Response"),
(8, "CATS - Caregiver Report Ages 3-6", "Score"),
(9, "CATS - Caregiver Report Ages 7-17", "Score"),
(10, "CATS - Youth Report", "Score"),
(11, "CPSS", "Total"),
(12, "CPSS Caregiver", "Total"),
(13, "CPSS-5-I", "Total"),
(14, "CPSS-5-P", "Total"),
(15, "CPSS-5-SR", "Total"),
(16, "CSBI", "CSBI Total (T-SCORE)"),
(17, "CSBI", "DRSB (T-SCORE)"),
(18, "CSBI", "SASI (T-SCORE)"),
(19, "Eyberg Child Behavior", "Intensity Raw Score")
]
# CAC_AGENCY
def generate_cac_agency():
    data = []
    fake = Faker()
    fake.seed_instance(0)
    for cac in cac_data:
        for _ in range(CAC_TO_AGENCY_RATIO):
            agency = {}
            # Data to be generated
            agency["agency_id"] = fake.unique.random_number(digits=8)
            agency["cac_id"] = cac["cac_id"]
            city = fake.unique.city()                     
            agency["agency_name"] = city + " Agency"
            agency["addr_line_1"] = fake.street_address()
            agency["addr_line_2"] = None
            agency["city"] = city
            agency["state_abbr"] = random.choice(state_abbreviations)
            agency["phone_number"] = fake.unique.numerify("(###)###-####")
            agency["zip_code"] = fake.postalcode()
            agency_data.append(agency)

# child_advocacy_center
def generate_child_advocacy_center():
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(CAC_TO_GENERATE):
        cac = {}
        # Data to be generated
        cac["cac_id"] = fake.unique.random_int(min = 1, max = CAC_TO_GENERATE + CAC_TO_GENERATE)
        city = fake.unique.city()
        cac["agency_name"] = city + " Child Advocacy Center"
        cac["addr_line_1"] = fake.street_address()
        cac["addr_line_2"] = None
        cac["city"] = city
        cac["state_abbr"] = random.choice(state_abbreviations)
        cac["phone_number"] = fake.unique.numerify("(###)###-####")
        cac["zip_code"] = fake.postalcode()
        cac_data.append(cac)

# TODO: Fix Nones
def generate_person(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        person = {}
        
        person["cac_id"] = random.choice(cac_data)["cac_id"]        # Choose a random cac
        person["person_id"] = fake.unique.random_number(digits=10)
        # Generates a male or female randomly.
        x = 0 if fake.random_int(min=0, max=1) == 0 else 1
        person["first_name"] = fake.first_name_male() if x == 0 else fake.first_name_female()
        person["middle_initial"] = fake.first_name_male()[0]  # Middle Initial
        person["last_name"] = fake.last_name_male() if x == 0 else fake.last_name_female()
        person["suffix"] = None
        person["birthdate"] = fake.date_of_birth(minimum_age=3, maximum_age=100).strftime('%d-%m-%Y')
        #TODO: Put this in a utility file
        birthdate = datetime.strptime(person["birthdate"], '%d-%m-%Y')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        person["gender"] = "M" if x == 0 else "F"
        person["language"] = fake.language_name()
        person["race"] = random.choice(races)
        person["religion"] = random.choice(religions)
        person["prior_convictions"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["convicted_against_children"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["sexual_offender"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["sexual_predator"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person_data.append(person)

#TODO: Figure out how this exactly works, is there multiple of these types of cases per person.
def generator_case_person(amount: int):
    fake = Faker()
    fake.add_provider(SchoolProvider)
    fake.seed_instance(0)
    for _ in range(amount):
        person  = random.choice(person_data)   
        case = {}
             
        case["person_id"] = person["person_id"]
        case["case_id"] = fake.unique.random_number(digits = 9)
        case["cac_id"] = person["cac_id"]
        birthdate = datetime.strptime(person["birthdate"], '%d-%m-%Y')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        # TODO: Check if it is Months / Days
        case["age"] = age
        case["age_unit"] = "year"
        case["addr_line_1"] = fake.street_address()
        case["addr_line_2"] = None
        city = fake.unique.city()
        case["city"] = city
        case["state_abbr"] = random.choice(state_abbreviations)
        case["zip_code"] = fake.postalcode()
        case["phone_number"] = fake.unique.numerify("(###)###-####")
        #FIXME: Set Chances / NULL
        case["phone_number"] = fake.unique.numerify("(###)###-####")
        case["phone_number"] = fake.unique.numerify("(###)###-####")
        school_data = fake.school_object()
        case["school_or_employer"] = school_data["school"] if age < 18 else fake.job()
        case["custody"] = fake.boolean()
        #TODO: Get Clarification on these
        case["education_level"] = school_data["level"] if age < 18 else random.choice(["GED", "No_GED", "Associates", "Bachelors", "Masters", "Doctorate"])
        case["income_level"] = random.choice(["Low", "Medium", "High"])
        #FIXME: AGE CHECK PLEASE ZANE
        case["martial_status"] = random.choice(["Single", "Married", "Divocred", "Widowed", "Seperated", "Anullued"])
        #TODO: Get Clarification
        case["relationship"] = "placeholder"
        case["case_role"] = random.choice(["Victim", "Family", "Aggressor"])
        case["same_household"] = fake.boolean()
        case["victim_status_id"] = fake.unique.random_number(digits = 8)
        case_person_data.append(case)
        
def generator_cac_case(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    counter = 0
    for _ in range(amount):
        person = random.choice(case_person_data)
        case = {}
        
        case["cac_id"] = person["cac_id"]
        case["case_id"] = person["case_id"]
        # Autogenerated case number that contains the year the case was created 
        # followed by a dash and an sequential integer indicating the ordinal value that the case was entered.
        case_date = fake.date()
        year = case_date[0:5]           #YYYY-
        case["case_number"] = year + str(counter)
        counter += 1
        case["cac_recieved_date"] = case_date
        case["case_closed_date"] = random.choice([fake.date_time_between(start_date=datetime.strptime(case_date, "%Y-%m-%d")), None])
        case["case_reason_id"] = fake.unique.random_number(digits = 8) if case["case_closed_date"] != None else None
        case["created_date"] = case_date
        #FIXME: Think of how to do this part
        case["mh_lead_employee_id"] = None
        case["mh_agency_id"] = None
        case["mh_case_number"] = None
        case["mh_mdt_ready"] = None
        case["mh_na"] = None
        case["mh_referral_date"] = None
        case["mh_therapy_accepted"] = None
        case["mh_therapy_complete_date"] = None
        case["mh_therapy_end_reason_id"] = None
        case["mh_therapy_offered_date"] = None
        case["mh_therapy_record_created"] = None
        case["va_agency_id"] = None
        case["va_case_number"] = None
        case["va_claim_denied_reason"] = None
        case["va_claim_number"] = None
        case["va_claim_status_id"] = None
        case["va_have_birth_cert"] = None
        case["va_have_police_report"] = None
        case["va_mdt_ready"] = None
        case["va_na"] = None
        case["va_referral_agency_id"] = None
        case["va_referral_date"] = None
        case["va_services_accepted"] = None
        case["va_services_end_date"] = None
        case["va_services_offered_date"] = None
        cac_case_data.append(case)
        
        
def generator_case_va_session_log(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        session = {}
        person = random.choice(cac_case_data)
        session["cac_id"] = person["cac_id"]
        session["case_id"] = person["case_id"]
        session["case_va_session_id"] = fake.unique.random_number(digits = 9)
        session["start_time"], session["end_time"] = util.generate_meeting_times()
        session["va_provider_agency_id"] = util.find_column(key = person["cac_id"], column="cac_id", table=agency_data, value="agency_id")
        #[ ] Not sure if this is the right format for this object, need to check.
        session["session_date"] = fake.date_time_between(start_date=datetime.strptime(person["cac_recieved_date"], "%Y-%m-%d"))
        session["session_status"] = fake.random_int(min=0, max=7)
        
        case_va_session_log_data.append(session)
        
def generator_case_va_session_attendee(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        session = {}
        case = random.choice(case_va_session_log_data)
        session["case_id"] = case["case_id"]
        session["case_va_session_attendee_id"] = fake.unique.random_number(digits = 7)
        session["case_va_session_id"] = case["case_va_session_id"]
        person = random.choice(person_data)
        session["person_id"] = person["person_id"]
        
        case_va_session_attendee_data.append(session)
        
def generator_case_va_session_service(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        session = {}
        case = random.choice(case_va_session_log_data)
        
        session["cac_id"] = case["cac_id"] 
        session["case_va_session_id"] = case["case_va_session_id"] 
        session["case_va_session_service_id"] = fake.unique.random_number(digits = 10)
        #FIXME: Check what this can be
        session["service_type_id"] = None
        
        case_va_session_service_data.append(session)

def generator_case_mh_assessments_instruments(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for temp in assessment_instrument:
        instrument = {}
        instrument["instruments_id"] = temp[0]
        instrument["mh_assessment_name"] = temp[1]
        
        case_mh_assessment_instruments_data.append(instrument)
        
def generator_case_mh_assessments(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        assessment = {}
        case = random.choice(cac_case_data)
        assessment["cac_id"] = case["cac_id"]
        assessment["case_id"] = case["case_id"]
        #FIXME: Ask about this value
        assessment["assessment_id"] = fake.unique.random_number(digits = 6)
        assessment["mh_provider_agency_id"] = util.find_column(key = case["cac_id"], column="cac_id", table=agency_data, value="agency_id")
        #FIXME: What does this mean
        assessment["timing_id"] = None
        #FIXME: repeat, what to do here
        # asssessment["assessment_id"] = ...
        #TODO: Fill in
        assessment["session_date"] = None
        assessment["agency_id"] = util.find_column(key = case["cac_id"], column="cac_id", table=agency_data, value="agency_id")
        assessment["provider_employee_id"] = None
        temp = random.choice(assessment_instrument)
        assessment["assessment_instrument_id"] = temp[0]
        assessment["comments"] = None
        
        case_mh_assessments_data.append(assessment)
        
def generator_case_mh_assessment_measure_scores(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        assessment = {}
        case = random.choice(case_mh_assessments_data)
        assessment["score_id"] = fake.unique.random_number(digits = 6)
        assessment["cac_id"] = case["cac_id"]
        assessment["case_id"] = case["case_id"]
        assessment["assessment_id"] = case["assessment_id"]
        assessment["instruments_id"] = case["assessment_instrument_id"]
        # FIXME: pick a value
        assessment["mh_assessment_scores"] = None
        
        case_mh_assessment_measure_scores_data.append(assessment)

def generator_mh_assessment_diagnosis_log(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        case = random.choice(cac_case_data)
        log = {}
        log["case_id"] = case["case_id"]
        log["diagonsis_date"] = fake.date()
        log["mh_provider_agency"] = None
        
        case_mh_diagonosis_log_data.append(log)
        
def generator_mh_session_log_enc(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        case = random.choice(cac_case_data)
        log = {}
        log["cac_id"] = case["cac_id"]
        log["case_id"] = case["case_id"]
        log["case_mh_session_id"] = fake.unique.random_number(digits = 8)
        log["comments"] = None
        log["start_time"] = None
        log["end_time"] = None
        log["intervention_id"] = None
        log["location_id"] = None
        log["onsite"] = None
        log["provider_agency_id"] = None
        log["provider_employee_id"] = None
        log["session_date"] = fake.date()
        log["session_status_id"] = fake.random_int(min=0, max=9, step = 1)
        log["session_type_id"] = None
        log["reccuring"] = None
        log["recurring_fre"] = None
        log["recurring_duration"] = None
        log["recurring_duration_unit"] = None
        
        case_mh_session_log_enc_data.append(log)
        
def generator_mh_treatment_plan(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        treatment = {}
        case = random.choice(cac_case_data)
        treatment["authorized_status_id"] = fake.random_int(min=0, max=5, step = 1)
        treatment["cac_id"] = case["cac_id"]
        treatment["case_id"] = case["case_id"]
        treatment["duration"] = None
        # FIXME: CHECK THIS LATER CUZ IM TOO TIRED TO UNDERSTAND
        treatment["duration_unit"] = None
        treatment["id"] = fake.unique.random_number(digits = 8)
        treatment["planned_end_date"] = None
        treatment["planned_review_date"] = None
        treatment["planned_start_date"] = None
        treatment["provider_agency_id"] = None
        treatment["provider_employee_id"] = None
        treatment["treatment_model_id"] = None
        treatment["treatment_plan_date"] = None
        
        case_mh_treatment_plans_data.append(treatment)
        
        
if __name__ == "__main__":
    print("[bold blue]NCA-Trak-Mock Data Generator")
    print("[yellow]How many data entries would you like to be generated?")
    n = int(input())
    print("[yellow]Generating Data...")
    # Call to make
    # TODO: Clean up calls, idk how yet...
    generate_child_advocacy_center()
    generate_cac_agency()
    generate_person(amount = n)
    generator_case_person(amount= n * n)
    generator_cac_case(amount= n)
    generator_case_va_session_log(amount=n // 2)
    generator_case_va_session_attendee(amount=n // 4)
    generator_case_va_session_service(n // 4)

    
    # Print Testing
    #print(cac_data)
    #print(agency_data)
    #print(person_data)
    #print(case_person_data)
    print(cac_case_data)
    print(case_va_session_log_data)
    print(case_va_session_attendee_data)
    print(case_va_session_service_data)
    