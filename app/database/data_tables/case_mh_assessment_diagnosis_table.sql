CREATE TABLE case_mh_assessment_diagnosis (
    case_id INTEGER NOT NULL,
    diagnosis_date DATE NOT NULL,
    mh_provider_agency_id INTEGER,
    FOREIGN KEY(case_id) REFERENCES cac_case(case_id),
    FOREIGN KEY(mh_provider_agency_id) REFERENCES cac_agency(agency_id)
);