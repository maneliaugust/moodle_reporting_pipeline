
CREATE TABLE IF NOT EXISTS moodle_learners (

    user_id INTEGER PRIMARY KEY,

    firstname VARCHAR(150),
    lastname VARCHAR(150),
    fullname VARCHAR(300),
    email VARCHAR(255),

    first_access TIMESTAMPTZ,
    last_access TIMESTAMPTZ,
    last_course_access TIMESTAMPTZ,

    course_count INTEGER,

    extracted_at TIMESTAMPTZ NOT NULL
);


CREATE TABLE IF NOT EXISTS moodle_activity_reports (

    id VARCHAR(100) PRIMARY KEY,

    coursename VARCHAR(255),
    groupname VARCHAR(255),

    userid INTEGER NOT NULL,
    firstname VARCHAR(150),
    lastname VARCHAR(150),

    activitytype VARCHAR(50),
    activityname VARCHAR(500),

    grade NUMERIC(10, 2),

    duedate TIMESTAMPTZ,
    submissiondate TIMESTAMPTZ,
    timemodified TIMESTAMPTZ,

    submissionstatus VARCHAR(50),

    extracted_at TIMESTAMPTZ NOT NULL
);


CREATE TABLE IF NOT EXISTS moodle_pipeline_run_history (

    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,

    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,

    records_fetched INTEGER DEFAULT 0,
    records_transformed INTEGER DEFAULT 0,
    records_loaded INTEGER DEFAULT 0,

    status VARCHAR(20) NOT NULL,

    error_message TEXT
);


CREATE TABLE IF NOT EXISTS moodle_extraction_tracking (

    pipeline_name VARCHAR(100) PRIMARY KEY,

    last_successful_extraction TIMESTAMPTZ,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);