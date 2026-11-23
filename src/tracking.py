
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


def get_last_successful_extraction(pipeline_name):

    engine = get_database_engine()

    query = text("""
        SELECT last_successful_extraction
        FROM moodle_extraction_tracking
        WHERE pipeline_name = :pipeline_name;
    """)

    try:
        with engine.connect() as connection:
            timestamp = connection.execute(
                query,
                {"pipeline_name": pipeline_name}
            ).scalar()

        return timestamp

    finally:
        engine.dispose()


def update_last_successful_extraction(
        pipeline_name, 
        extraction_start_time
):

    engine = get_database_engine()

    query = text("""
        INSERT INTO moodle_extraction_tracking (
            pipeline_name,
            last_successful_extraction,
            updated_at
        )
        VALUES (
            :pipeline_name,
            :extraction_start_time,
            NOW()
        )
        ON CONFLICT (pipeline_name)
        DO UPDATE SET
            last_successful_extraction = EXCLUDED.last_successful_extraction,
            updated_at = NOW()
        RETURNING last_successful_extraction;
    """)

    try:
        with engine.begin() as connection:
            timestamp = connection.execute(
                query,
                {"pipeline_name": pipeline_name,
                "extraction_start_time": extraction_start_time
                }
            ).scalar()

        print(f"Extraction checkpoint updated: {timestamp}")

        return timestamp

    finally:
        engine.dispose()


def get_extraction_start_time():

    engine = get_database_engine()

    query = text("SELECT NOW();")

    try:
        with engine.connect() as connection:
            timestamp = connection.execute(query).scalar()

        return timestamp

    finally:
        engine.dispose()
