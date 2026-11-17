
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


def get_database_engine():

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(
        connection_url,
        pool_pre_ping=True
    )

    return engine


def test_database_connection():

    engine = get_database_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database();")
        )

        database_name = result.scalar()

    print("PostgreSQL connection successful!")
    print(f"Connected database: {database_name}")

    return engine


def create_tables():

    engine = get_database_engine()

    with open("sql/create_tables.sql", "r") as file:
        sql_script = file.read()

    with engine.begin() as connection:
        connection.exec_driver_sql(sql_script)

    print("Moodle database tables created successfully!")

    engine.dispose()