
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

    # Convert Pandas missing values (NaT/NaN) to Python None
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
