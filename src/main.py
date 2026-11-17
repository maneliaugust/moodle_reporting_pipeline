
from src.extract import get_enrolled_users
from src.transform import transform_learners
from src.validate import validate_learners
from src.database import create_tables
from src.load import load_learners
from src.tracking import start_pipeline_run, update_pipeline_run


def main():

    print("Preparing database tables...")
    create_tables()

    run_id = start_pipeline_run("Moodle Reporting Pipeline")

    records_fetched = 0
    records_transformed = 0
    records_loaded = 0

    try:
        print("\nExtracting Moodle learner data...")

        users = get_enrolled_users(6)
        records_fetched = len(users)

        print(f"Users retrieved: {records_fetched}")

        print("\nTransforming learner data...")

        df = transform_learners(users)
        records_transformed = len(df)

        print(f"Learners transformed: {records_transformed}")

        print("\nStarting data quality validation...")

        if not validate_learners(df):
            raise ValueError("Data quality validation failed.")

        print("\nLoading learner data into PostgreSQL...")

        load_learners(df)
        records_loaded = len(df)

        update_pipeline_run(
            run_id,
            records_fetched,
            records_transformed,
            records_loaded,
            "Success"
        )

        print("\nMoodle reporting pipeline completed successfully!")

    except Exception as error:

        update_pipeline_run(
            run_id,
            records_fetched,
            records_transformed,
            records_loaded,
            "Failed",
            str(error)
        )

        print(f"\nPipeline failed: {error}")


if __name__ == "__main__":
    main()
