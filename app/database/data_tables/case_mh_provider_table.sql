CREATE TABLE case_mh_provider (
    provider_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    case_number VARCHAR(20),
    agency_id INTEGER,
    lead_employee_id INTEGER,
    provider_type_id INTEGER,
    therapy_offered_date DATE,
    therapy_accepted BOOLEAN,
    therapy_complete_date DATE,
    therapy_end_reason VARCHAR(255),
    therapy_record_created BOOLEAN,
    FOREIGN KEY(case_id) REFERENCES cac_case(case_id),
    FOREIGN KEY(agency_id) REFERENCES cac_agency(agency_id),
    FOREIGN KEY(lead_employee_id) REFERENCES employee(employee_id)
);