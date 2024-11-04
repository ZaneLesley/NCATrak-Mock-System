INSERT INTO case_mh_session_log_enc (
    cac_id,
    case_id,
    case_mh_session_id,
    comments,
    start_time,
    end_time,
    intervention_id,
    location_id,
    onsite,
    provider_agency_id,
    provider_employee_id,
    session_date,
    session_status_id,
    session_type_id,
    recurring,
    recurring_fre,
    recurring_duration,
    recurring_duration_unit
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);