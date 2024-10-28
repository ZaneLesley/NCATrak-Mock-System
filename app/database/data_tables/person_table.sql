CREATE TABLE person (
    cac_id SMALLINT NOT NULL,
    person_id INTEGER PRIMARY KEY,
    first_name VARCHAR(256),
    middle_name VARCHAR(256),
    last_name VARCHAR(256),
    suffix VARCHAR(256),
    date_of_birth date,
    gender VARCHAR(1),
    language_id INTEGER,
    race_id INTEGER,
    religion_id INTEGER,
    prior_convictions BOOLEAN,
    convicted_against_children BOOLEAN,
    sex_offender BOOLEAN,
    sex_predator BOOLEAN,
    FOREIGN KEY(cac_id) REFERENCES child_advocacy_center(cac_id)
);