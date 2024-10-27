INSERT INTO case_va_session (
    case_va_session_id,
    cac_id,
    case_id,
    session_date,
    session_start_time,
    session_end_time,
    va_provider_agency_id,
    session_status
) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);