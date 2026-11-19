
from src.extract import (
    get_enrolled_users,
    call_moodle_api
)

from src.transform import (
    transform_learners,
    transform_activity_reports
)

from src.validate import (
    validate_learners,
    validate_activity_reports
)

from src.database import create_tables

from src.load import (
    load_learners,
    load_activity_reports
)

from src.tracking import start_pipeline_run, update_pipeline_run
from src.logger_config import setup_logger


def main():

    logger = setup_logger()

    records_fetched = 0
    records_transformed = 0
    records_loaded = 0
    run_id = None

    try:

        logger.info("Preparing database tables...")
        create_tables()

        run_id = start_pipeline_run("Moodle Reporting Pipeline")

        logger.info("Moodle reporting pipeline started.")

        # ------------------------------------------------
        # LEARNER DATA
        # ------------------------------------------------

        logger.info("Extracting Moodle learner data...")

        users = get_enrolled_users(6)

        learner_records_fetched = len(users)
        records_fetched += learner_records_fetched

        logger.info(f"Users retrieved: {learner_records_fetched}")

        logger.info("Transforming learner data...")

        learner_df = transform_learners(users)

        learner_records_transformed = len(learner_df)
        records_transformed += learner_records_transformed

        logger.info(
            f"Learners transformed: {learner_records_transformed}"
        )

        logger.info("Validating learner data...")

        if not validate_learners(learner_df):
            raise ValueError("Learner data validation failed.")

        logger.info("Learner data validation passed.")

        logger.info("Loading learner data into PostgreSQL...")

        load_learners(learner_df)

        learner_records_loaded = len(learner_df)
        records_loaded += learner_records_loaded

        logger.info(
            f"Learner records loaded: {learner_records_loaded}"
        )

        # ------------------------------------------------
        # ACTIVITY REPORT DATA
        # ------------------------------------------------

        logger.info("Extracting Moodle activity reports...")

        activity_records = call_moodle_api(
            "local_grades_get_activity_reports"
        )

        activity_records_fetched = len(activity_records)
        records_fetched += activity_records_fetched

        logger.info(
            f"Activity records retrieved: {activity_records_fetched}"
        )

        logger.info("Transforming activity report data...")

        activity_df = transform_activity_reports(activity_records)

        activity_records_transformed = len(activity_df)
        records_transformed += activity_records_transformed

        logger.info(
            f"Activity records transformed: {activity_records_transformed}"
        )

        logger.info("Validating activity report data...")

        if not validate_activity_reports(activity_df):
            raise ValueError("Activity report validation failed.")

        logger.info("Activity report validation passed.")

        logger.info("Loading activity reports into PostgreSQL...")

        load_activity_reports(activity_df)

        activity_records_loaded = len(activity_df)
        records_loaded += activity_records_loaded

        logger.info(
            f"Activity records loaded: {activity_records_loaded}"
        )

        # ------------------------------------------------
        # PIPELINE COMPLETION
        # ------------------------------------------------

        update_pipeline_run(
            run_id,
            records_fetched,
            records_transformed,
            records_loaded,
            "Success"
        )

        logger.info("Moodle reporting pipeline completed successfully.")

        logger.info(f"Total records fetched: {records_fetched}")
        logger.info(f"Total records transformed: {records_transformed}")
        logger.info(f"Total records loaded: {records_loaded}")

    except Exception as error:

        logger.exception("Moodle reporting pipeline failed.")

        if run_id is not None:

            try:

                update_pipeline_run(
                    run_id,
                    records_fetched,
                    records_transformed,
                    records_loaded,
                    "Failed",
                    str(error)
                )

            except Exception:

                logger.exception(
                    "Failed to update pipeline run history."
                )

        raise


if __name__ == "__main__":
    main()
