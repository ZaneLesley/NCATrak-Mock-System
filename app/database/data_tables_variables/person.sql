INSERT INTO person (
    cac_id,
    person_id,
    first_name,
    middle_name,
    last_name,
    suffix,
    date_of_birth,
    gender,
    language_id,
    race_id,
    religion_id ,
    prior_convictions,
    convicted_against_children,
    sex_offender,
    sex_predator
) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);