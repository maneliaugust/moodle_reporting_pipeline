
import pandas as pd
from sqlalchemy import text

from src.database import get_database_engine


def load_learners(df):

    engine = get_database_engine()

    upsert_query = text("""
        INSERT INTO moodle_learners (
            user_id,
            firstname,
            lastname,
            fullname,
            email,
            first_access,
            last_access,
            last_course_access,
            course_count,
            extracted_at
        )
        VALUES (
            :user_id,
            :firstname,
            :lastname,
            :fullname,
            :email,
            :first_access,
            :last_access,
            :last_course_access,
            :course_count,
            :extracted_at
        )
        ON CONFLICT (user_id)
        DO UPDATE SET
            firstname = EXCLUDED.firstname,
            lastname = EXCLUDED.lastname,
            fullname = EXCLUDED.fullname,
            email = EXCLUDED.email,
            first_access = EXCLUDED.first_access,
            last_access = EXCLUDED.last_access,
            last_course_access = EXCLUDED.last_course_access,
            course_count = EXCLUDED.course_count,
            extracted_at = EXCLUDED.extracted_at;
    """)

    clean_df = df.astype(object).where(
        pd.notna(df),
        None
    )

    records = clean_df.to_dict(orient="records")

    try:

        with engine.begin() as connection:

            connection.execute(
                upsert_query,
                records
            )

        print(
            f"Learner records loaded successfully: {len(records)}"
        )

    finally:
        engine.dispose()


def load_activity_reports(df):

    if df.empty:
        print("No activity reports to load.")
        return

    engine = get_database_engine()

    upsert_query = text("""
        INSERT INTO moodle_activity_reports (
            id,
            coursename,
            groupname,
            userid,
            firstname,
            lastname,
            activitytype,
            activityname,
            grade,
            duedate,
            submissiondate,
            timemodified,
            submissionstatus,
            extracted_at
        )
        VALUES (
            :id,
            :coursename,
            :groupname,
            :userid,
            :firstname,
            :lastname,
            :activitytype,
            :activityname,
            :grade,
            :duedate,
            :submissiondate,
            :timemodified,
            :submissionstatus,
            :extracted_at
        )
        ON CONFLICT (id)
        DO UPDATE SET
            coursename = EXCLUDED.coursename,
            groupname = EXCLUDED.groupname,
            userid = EXCLUDED.userid,
            firstname = EXCLUDED.firstname,
            lastname = EXCLUDED.lastname,
            activitytype = EXCLUDED.activitytype,
            activityname = EXCLUDED.activityname,
            grade = EXCLUDED.grade,
            duedate = EXCLUDED.duedate,
            submissiondate = EXCLUDED.submissiondate,
            timemodified = EXCLUDED.timemodified,
            submissionstatus = EXCLUDED.submissionstatus,
            extracted_at = EXCLUDED.extracted_at;
    """)

    clean_df = df.astype(object).where(
        pd.notna(df),
        None
    )

    records = clean_df.to_dict(orient="records")

    try:

        with engine.begin() as connection:

            connection.execute(
                upsert_query,
                records
            )

        print(
            f"Activity records loaded successfully: {len(records)}"
        )

    finally:
        engine.dispose()
