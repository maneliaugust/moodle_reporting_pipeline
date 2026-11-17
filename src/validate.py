
def validate_learners(df):

    errors = []

    # Check whether the dataset is empty
    if df.empty:
        errors.append("Dataset is empty.")

    # Check for missing learner IDs
    if df["user_id"].isna().any():
        errors.append("Missing learner IDs found.")

    # Check for duplicate learner IDs
    if df["user_id"].duplicated().any():
        errors.append("Duplicate learner IDs found.")

    # Check for missing names
    if df["firstname"].isna().any():
        errors.append("Missing first names found.")

    if df["lastname"].isna().any():
        errors.append("Missing last names found.")

    # Check for missing email addresses
    if df["email"].isna().any():
        errors.append("Missing email addresses found.")

    # Check course counts
    if (df["course_count"] < 0).any():
        errors.append("Invalid course counts found.")

    # Display validation results
    if errors:
        print("\nData quality validation FAILED!")

        for error in errors:
            print(f"- {error}")

        return False

    print("\nData quality validation PASSED!")

    return True
