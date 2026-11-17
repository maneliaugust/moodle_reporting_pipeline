
import pandas as pd
from datetime import datetime, timezone


def transform_learners(users):

    learners = []

    for user in users:

        roles = user.get("roles", [])

        role_names = [
            role.get("shortname")
            for role in roles
        ]

        if "student" not in role_names:
            continue

        learners.append({
            "user_id": user.get("id"),
            "firstname": user.get("firstname"),
            "lastname": user.get("lastname"),
            "fullname": user.get("fullname"),
            "email": user.get("email"),
            "first_access": user.get("firstaccess"),
            "last_access": user.get("lastaccess"),
            "last_course_access": user.get("lastcourseaccess"),
            "course_count": len(user.get("enrolledcourses", []))
        })

    df = pd.DataFrame(learners)

    timestamp_columns = [
        "first_access",
        "last_access",
        "last_course_access"
    ]

    for column in timestamp_columns:

        # Convert zero timestamps to missing values
        timestamps = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        timestamps = timestamps.where(timestamps > 0)

        df[column] = pd.to_datetime(
            timestamps,
            unit="s",
            utc=True,
            errors="coerce"
        )

    df["extracted_at"] = datetime.now(timezone.utc)

    return df
