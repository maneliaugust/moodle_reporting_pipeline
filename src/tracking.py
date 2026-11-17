
from sqlalchemy import text

from src.database import get_database_engine


def start_pipeline_run(pipeline_name):

    engine = get_database_engine()

    query = text("""
        INSERT INTO moodle_pipeline_run_history (
            pipeline_name,
            started_at,
            status
        )
        VALUES (
            :pipeline_name,
            NOW(),
            'Running'
        )
        RETURNING run_id;
    """)

    try:
        with engine.begin() as connection:
            run_id = connection.execute(
                query,
                {"pipeline_name": pipeline_name}
            ).scalar()

        print(f"Pipeline run started. Run ID: {run_id}")

        return run_id

    finally:
        engine.dispose()


def update_pipeline_run(
    run_id,
    records_fetched,
    records_transformed,
    records_loaded,
    status,
    error_message=None
):

    engine = get_database_engine()

    query = text("""
        UPDATE moodle_pipeline_run_history
        SET
            completed_at = NOW(),
            records_fetched = :records_fetched,
            records_transformed = :records_transformed,
            records_loaded = :records_loaded,
            status = :status,
            error_message = :error_message
        WHERE run_id = :run_id;
    """)

    try:
        with engine.begin() as connection:
            connection.execute(
                query,
                {
                    "run_id": run_id,
                    "records_fetched": records_fetched,
                    "records_transformed": records_transformed,
                    "records_loaded": records_loaded,
                    "status": status,
                    "error_message": error_message
                }
            )

        print(f"Pipeline run {run_id} updated: {status}")

    finally:
        engine.dispose()
