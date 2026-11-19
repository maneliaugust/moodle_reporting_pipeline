
def validate_learners(df):

    errors = []

    if df.empty:
        errors.append("Dataset is empty.")

    if df["user_id"].isna().any():
        errors.append("Missing learner IDs found.")

    if df["user_id"].duplicated().any():
        errors.append("Duplicate learner IDs found.")

    if df["firstname"].isna().any():
        errors.append("Missing first names found.")

    if df["lastname"].isna().any():
        errors.append("Missing last names found.")

    if df["email"].isna().any():
        errors.append("Missing email addresses found.")

    if (df["course_count"] < 0).any():
        errors.append("Invalid course counts found.")

    if errors:
        print("\nLearner data validation FAILED!")

        for error in errors:
            print(f"- {error}")

        return False

    print("\nLearner data validation PASSED!")

    return True


def validate_activity_reports(df):

    errors = []

    if df.empty:
        errors.append("Activity report dataset is empty.")
    else:

        # Check activity IDs
        if df["id"].isna().any():
            errors.append("Missing activity IDs found.")

        if df["id"].duplicated().any():
            errors.append("Duplicate activity IDs found.")

        # Check learner IDs
        if df["userid"].isna().any():
            errors.append("Missing learner IDs in activity reports.")

        # Check activity names
        if df["activityname"].isna().any():
            errors.append("Missing activity names found.")

        # Check grades
        if (df["grade"].dropna() < 0).any():
            errors.append("Negative grades found.")

        # Check submission statuses
        valid_statuses = ["late", "missed", "pending"]

        invalid_statuses = ~df["submissionstatus"].isin(valid_statuses)

        if invalid_statuses.any():
            errors.append("Invalid submission statuses found.")

    if errors:
        print("\nActivity report validation FAILED!")

        for error in errors:
            print(f"- {error}")

        return False

    print("\nActivity report validation PASSED!")

    return True
