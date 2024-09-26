CREATE TABLE person (
    cac_id SMALLINT NOT NULL,
    person_id INTEGER PRIMARY KEY,
    first_name VARCHAR(256),
    middle_name VARCHAR(256),
    last_name VARCHAR(256),
    suffix VARCHAR(256),
    birth_date date,
    gender VARCHAR(1),
    lang VARCHAR(50),
    race VARCHAR(50),
    religion VARCHAR(50),
    prior_convictions BOOLEAN,
    convicted_against_children BOOLEAN,
    sex_offender BOOLEAN,
    sex_predator BOOLEAN,
    FOREIGN KEY(cac_id) REFERENCES child_advocacy_center(cac_id)
);