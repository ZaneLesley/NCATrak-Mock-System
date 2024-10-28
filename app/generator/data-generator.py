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
child_advocacy_center_data = []
cac_agency_data = []
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

# (id, name)
treatment_models = [
(0, "AF-CBT", "Assertiveness"),
(1, "AF-CBT",	"Assessment"),
(2, "AF-CBT",	"Behavior Recognition and Management"),
(3, "AF-CBT",	"Clarification"),
(4, "AF-CBT", "Communication"),
(5, "AF-CBT", "Emotional Regulation"),
(6, "AF-CBT", "Graduation"),
(7, "AF-CBT", "Imaginal Exposure"),
(8, "AF-CBT", "Orientation"),
(9, "AF-CBT", "Problem-Solving"),
(10, "AF-CBT", "Psychoeducation"),
(11, "AF-CBT", "Reviewing Thoughts"),
(12, "AF-CBT", "Social Skills")
]

# (Attribute Group, Attributes)
attribute = [
("Client Affect",	"Apathetic"),
("Client Affect",	"Appropriate"),
("Client Affect",	"Blunted"),
("Client Affect",	"Exaggerated"),
("Client Affect",	"Flat"),
("Client Affect",	"Inappropriate"),
("Client Affect",	"Irritable"),
("Client Affect",	"Labile"),
("Client Affect",	"Other"),
("Client Affect",	"Pleasant"),
("Client Affect",	"Stabile"),
("Client Mood",	"Angry"),
("Client Mood",	"Anxious"),
("Client Mood",	"Depressed"),
("Client Mood",	"Euphoric"),
("Client Mood",	"Euthymic"),
("Client Mood",	"Other"),
("Homicidal Ideation",	"Homicidal Ideation"),
("Homicidal Ideation",	"No Homicidal Ideation"),
("Suicidal Ideation",	"Not Suicidal"),
("Suicidal Ideation",	"Suicidal Ideation"),
("Suicidal Ideation",	"Suicidal Ideation and Plan"),
("Treatment Plan Progress",	"Met/Exceeded"),
("Treatment Plan Progress",	"Minimal"),
("Treatment Plan Progress",	"Moderate"),
("Treatment Plan Progress",	"None"),
("Treatment Plan Progress",	"Significant")
]

# child_advocacy_center
def generate_cac_agency():
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(CAC_TO_GENERATE):
        cac = {}
        # Data to be generated
        cac["cac_id"] = fake.unique.random_int(min = 1, max = CAC_TO_GENERATE + CAC_TO_GENERATE)
        city = fake.unique.city()
        cac["agency_name"] = city + " Child Advocacy Center"
        cac["address_line_1"] = fake.street_address()
        cac["address_line_2"] = None
        cac["city"] = city
        cac["state_abbr"] = random.choice(state_abbreviations)
        cac["phone_number"] = fake.unique.numerify("(###)###-####")
        cac["zip"] = fake.postalcode()
        child_advocacy_center_data.append(cac)

# CAC_AGENCY
def generate_child_advocacy_center():
    data = []
    fake = Faker()
    fake.seed_instance(0)
    for cac in child_advocacy_center_data:
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
            cac_agency_data.append(agency)

# TODO: Fix Nones
def generate_person(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        person = {}
        
        person["cac_id"] = random.choice(child_advocacy_center_data)["cac_id"]        # Choose a random cac
        person["person_id"] = fake.unique.random_number(digits=9)
        # Generates a male or female randomly.
        x = 0 if fake.random_int(min=0, max=1) == 0 else 1
        person["first_name"] = fake.first_name_male() if x == 0 else fake.first_name_female()
        person["middle_initial"] = fake.first_name_male() if x == 0 else fake.first_name_female()
        person["last_name"] = fake.last_name_male() if x == 0 else fake.last_name_female()
        person["suffix"] = None
        person["date_of_birth"] = fake.date_of_birth(minimum_age=3, maximum_age=100)
        #TODO: Put this in a utility file
        birthdate = person["date_of_birth"]
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        person["gender"] = "M" if x == 0 else "F"
        person["language_id"] = None
        person["race_id"] = None
        person["religion_id"] = None
        person["prior_convictions"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["convicted_against_children"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["sexual_offender"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["sexual_predator"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person_data.append(person)

def generator_cac_case(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    counter = 0
    for _ in range(amount):
        person = random.choice(person_data)
        case = {}
        
        case["cac_id"] = person["cac_id"]
        case["case_id"] = fake.unique.random_number(digits = 9)
        # Autogenerated case number that contains the year the case was created 
        # followed by a dash and an sequential integer indicating the ordinal value that the case was entered.
        case_date = fake.date_object()
        year = case_date.strftime("%Y")           #YYYY-
        case["case_number"] = year + str(counter)
        counter += 1
        case["cac_recieved_date"] = case_date
        case["case_closed_date"] = random.choice([fake.date_time_between(
            start_date=datetime.combine(case_date, datetime.min.time())).date(), None])
        case["closed_reason_id"] = fake.unique.random_number(digits = 8) if case["case_closed_date"] != None else None
        case["created_date"] = case_date
        #FIXME: Think of how to do this part
        case["mh_lead_employee_id"] = None
        case["mh_agency_id"] = None
        case["mh_case_number"] = None
        case["mh_mdt_ready"] = None
        case["mh_na"] = None
        case["mh_referral_agency_id"] = None
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
        
#TODO: Figure out how this exactly works, is there multiple of these types of cases per person.
def generator_case_person(amount: int):
    fake = Faker()
    fake.add_provider(SchoolProvider)
    fake.seed_instance(0)
    temp = cac_case_data.copy()
    for _ in range(amount):
        person  = random.choice(temp)
        temp.remove(person)   
        case = {}

        # FIXME: Is the person ID unique?
        case["person_id"] = util.find_column(key = person["cac_id"], column="cac_id", table=person_data, value="person_id")
        case["case_id"] = person["case_id"]
        case["cac_id"] = person["cac_id"]
        birthdate = util.find_column(key = person["cac_id"], column="cac_id", table=person_data, value="date_of_birth")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        # TODO: Check if it is Months / Days
        case["age"] = age
        case["age_unit"] = "year"
        case["address_line_1"] = fake.street_address()
        case["address_line_2"] = None
        city = fake.unique.city()
        case["city"] = city
        case["state_abbr"] = random.choice(state_abbreviations)
        case["zip"] = fake.postalcode()
        case["cell_phone_number"] = fake.unique.numerify("(###)###-####")
        #FIXME: Set Chances / NULL
        case["home_phone_number"] = fake.unique.numerify("(###)###-####")
        case["work_phone_number"] = fake.unique.numerify("(###)###-####")
        school_data = fake.school_object()
        case["custody"] = fake.boolean()
        case["education_level_id"] = None
        case["income_level_id"] = None
        case["marital_status_id"] = None
        case["relationship_id"] = None
        case["role_id"] = None
        case["same_household"] = fake.boolean()
        case["school_or_employer"] = school_data["school"] if age < 18 else fake.job()
        case["victim_status_id"] = fake.unique.random_number(digits = 8)
        case_person_data.append(case)
         
def generator_case_va_session_log(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        session = {}
        person = random.choice(cac_case_data)
        session["cac_id"] = person["cac_id"]
        session["case_id"] = person["case_id"]
        session["case_va_session_id"] = fake.unique.random_number(digits = 9)
        session["start_time"] = fake.date_time_between(start_date=person["cac_recieved_date"])
        session["end_time"] = util.generate_meeting_times(start_datetime=session["start_time"])
        session["va_provider_agency_id"] = util.find_column(key = person["cac_id"], column="cac_id", table=cac_agency_data, value="agency_id")
        #[ ] Not sure if this is the right format for this object, need to check.
        session["session_date"] = fake.date_time_between(start_date=person["cac_recieved_date"])
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
        assessment["mh_provider_agency_id"] = util.find_column(key = case["cac_id"], column="cac_id", table=cac_agency_data, value="agency_id")
        #FIXME: What does this mean
        assessment["timing_id"] = None
        #FIXME: repeat, what to do here
        # asssessment["assessment_id"] = ...
        #TODO: Fill in
        assessment["session_date"] = None
        assessment["assessment_date"] = None
        assessment["agency_id"] = util.find_column(key = case["cac_id"], column="cac_id", table=cac_agency_data, value="agency_id")
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
        # FIXME: determine a way to get specific values (from a, b depending on description)
        assessment["mh_assessment_scores"] = None
        
        case_mh_assessment_measure_scores_data.append(assessment)

def generator_mh_assessment_diagnosis_log(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        case = random.choice(cac_case_data)
        log = {}
        log["case_id"] = case["case_id"]
        log["diagonsis_date"] = fake.date_object()
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
        
# FIXME: Maybe Review and ensure this one is correct with case vs person
def generator_mh_session_attendee(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        person = random.choice(person_data)
        session = {}
        session["person_id"] = person["person_id"]
        session["cac_id"] = person["cac_id"]
        session["case_id"] = util.find_column(key = session["person_id"], column="person_id", table=case_person_data, value="case_id")
        session["case_mh_session_attendee_id"] = fake.unique.random_number(digits = 8)  
        session["case_mh_session_id"] = util.find_column(key = session["cac_id"], column="cac_id", table=case_mh_session_log_enc_data, value="case_mh_session_id")
        
        case_mh_session_attendee_data.append(session)
    
def generator_mh_session_attribute_group(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        attendee = random.choice(case_mh_session_attendee_data)
        group = {}
        group["id"] = fake.unique.random_number(digits = 7)
        group["cac_id"] = attendee["cac_id"]
        group["case_id"] = util.find_column(key = group["cac_id"], column="cac_id", table=cac_case_data, value="case_id")
        group["case_mh_session_id"] = attendee["case_mh_session_id"]
        temp = random.choice(attribute)
        group["attribute_group_description"] = temp[0]
        group["attributes"] = temp[1]
        group["attribute_value"] = fake.random_int(min=0, max=100)
        
        case_mh_attribute_group_data.append(group)
        
def generator_mh_provider_log(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        case = random.choice(cac_case_data)
        log = {}
        log["agency_id"] = util.find_column(key = case["cac_id"], column="cac_id", table=cac_agency_data, value="agency_id")
        log["case_id"] = case["case_id"]
        log["case_number"] = case["case_number"]
        log["id"] = fake.unique.random_number(digits = 5)
        log["lead_employee_id"] = None
        log["provider_type_id"] = None
        log["therapy_accepted"] = None
        log["therapy_complete_date"] = None
        log["therapy_end_reason_id"] = None
        log["therapy_offered_date"] = None
        log["therapy_record_created"] = None
        
        case_mh_provider_log_data.append(log)
        
def generator_mh_service_barriers(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        barrier = {}
        barrier["id"] = fake.unique.random_number(digits = 10)
        barrier["number_of_miles"] = None
        barrier["barrier_id"] = None
        
        case_mh_service_barriers_data.append(barrier)
        
def generator_mh_treatment_models(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for temp in treatment_models:
        instrument = {}
        instrument["id"] = temp[0]
        instrument["Name"] = temp[1]
        
        case_mh_treatment_models_data.append(instrument)
        
if __name__ == "__main__":
    print("[bold blue]NCA-Trak-Mock Data Generator")
    print("[yellow]How many data entries would you like to be generated?")
    n = int(input())
    print("[yellow]Generating Data...")
    # Call to make
    # TODO: Clean up calls, idk how yet...
    generate_cac_agency()
    generate_child_advocacy_center()
    generate_person(amount = n)
    generator_cac_case(amount= n * 2)
    generator_case_person(amount= n * 2)
    generator_case_va_session_log(amount=n // 2)
    generator_case_va_session_attendee(amount=n // 4)
    generator_case_va_session_service(n // 4)
    generator_case_mh_assessments_instruments(n // 4)
    generator_case_mh_assessments(n // 4)
    generator_case_mh_assessment_measure_scores(n // 4)
    generator_mh_assessment_diagnosis_log(n // 4)
    generator_mh_session_log_enc(n // 4)
    generator_mh_treatment_plan(n // 4)
    generator_mh_session_attendee(n // 4)
    generator_mh_session_attribute_group(n // 4)
    generator_mh_provider_log(n // 4)
    generator_mh_service_barriers(n // 4)
    generator_mh_treatment_models(n // 4)
    
    util.write_to_csv(data=cac_agency_data, name="cac_agency_data")
    util.write_to_csv(data=child_advocacy_center_data, name="child_advocacy_center_data")
    util.write_to_csv(data=person_data, name="person_data")
    util.write_to_csv(data=case_person_data, name="case_person_data")
    util.write_to_csv(data=cac_case_data, name="cac_case_data")
    util.write_to_csv(data=case_va_session_log_data, name="case_va_session_log_data")
    util.write_to_csv(data=case_va_session_attendee_data, name="case_va_session_attendee_data")
    util.write_to_csv(data=case_va_session_service_data, name="case_va_session_service_data")
    util.write_to_csv(data=case_mh_assessments_data, name="case_mh_assessments_data")
    util.write_to_csv(data=case_mh_assessment_instruments_data, name="case_mh_assessment_instruments_data")
    util.write_to_csv(data=case_mh_assessment_measure_scores_data, name="case_mh_assessment_measure_scores_data")
    util.write_to_csv(data=case_mh_diagonosis_log_data, name="case_mh_diagonosis_log_data")
    util.write_to_csv(data=case_mh_session_log_enc_data, name="case_mh_session_log_enc_data")
    util.write_to_csv(data=case_mh_treatment_plans_data, name="case_mh_treatment_plans_data")
    util.write_to_csv(data=case_mh_session_attendee_data, name="case_mh_session_attendee_data")
    util.write_to_csv(data=case_mh_attribute_group_data, name="case_mh_attribute_group_data")
    util.write_to_csv(data=case_mh_provider_log_data, name="case_mh_provider_log_data")
    util.write_to_csv(data=case_mh_service_barriers_data, name="case_mh_service_barriers_data")
    util.write_to_csv(data=case_mh_treatment_models_data, name="case_mh_treatment_models_data")
    #util.write_to_csv(data=state_data, name="state_data")
    #util.write_to_csv(data=employee_data, name="employee_data")
    #util.write_to_csv(data=employee_account_data, name="employee_account_data")
    # Print Testing
    """
    for key, value in case_mh_session_attendee_data[0].items():
        print(f"Key: {key}, {type(value)}, value: {value}")
    """
    #print(cac_agency_data)
    #print(child_advocacy_center_data)
    #print(person_data)
    #print(case_person_data)
    #print(cac_case_data)
    #print(case_va_session_log_data)
    #print(case_va_session_attendee_data)
    #print(case_va_session_service_data)
    #print(case_mh_assessments_data)
    #print(case_mh_assessment_instruments_data)
    #print(case_mh_assessment_measure_scores_data)
    #print(case_mh_diagonosis_log_data)
    #print(case_mh_session_log_enc_data)
    #print(case_mh_treatment_plans_data)
    #print(case_mh_session_attendee_data)
    #print(case_mh_attribute_group_data)
    #print(case_mh_provider_log_data)
    #print(case_mh_service_barriers_data)
    #print(case_mh_treatment_models_data)
    #print(state_data)
    #print(employee_data)
    #print(employee_account_data)
    