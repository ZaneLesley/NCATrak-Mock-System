CREATE TABLE case_va_session (
    case_va_session_id INTEGER PRIMARY KEY,
    cac_id SMALLINT NOT NULL,
    case_id INTEGER NOT NULL,
    session_date DATE,
    session_start_time VARCHAR(20),
    session_end_time VARCHAR(20),
    va_provider_agency_id INTEGER,
    session_status INTEGER,
    FOREIGN KEY(cac_id) REFERENCES child_advocacy_center(cac_id),
    FOREIGN KEY(case_id) REFERENCES cac_case(case_id),
    FOREIGN KEY(va_provider_agency_id) REFERENCES cac_agency(agency_id)
);