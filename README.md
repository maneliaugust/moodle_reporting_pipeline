# Moodle Reporting Pipeline – Python & PostgreSQL

## Project Overview

This project is an automated ETL (Extract, Transform, Load) pipeline that retrieves learner and activity data from a Moodle Learning Management System (LMS) using the Moodle REST API.

The pipeline uses Python and Pandas to extract, clean, transform and validate Moodle data before storing it in a separate PostgreSQL reporting database.

It supports learner reporting, activity reporting, incremental data extraction, data quality validation, UPSERT functionality and pipeline execution tracking.

The pipeline also maintains extraction checkpoints to track the last successful extraction and avoid repeatedly processing unchanged activity records.

## Technologies Used

- **Python** – ETL development and API integration
- **Moodle REST API** – Learner and activity data extraction
- **Pandas** – Data transformation and cleaning
- **PostgreSQL** – Reporting database
- **SQLAlchemy** – Database connectivity and queries
- **Requests** – API requests
- **Python-dotenv** – Environment variable management
- **Git & GitHub** – Version control

## Project Structure

```text
moodle_reporting_pipeline/
│
├── logs/
│
├── sql/
│   └── create_tables.sql
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── database.py
│   ├── load.py
│   ├── tracking.py
│   └── logger_config.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ETL Pipeline Process

### 1. Extraction

The pipeline connects to Moodle through its REST API to retrieve learner and activity information.

**Learner data extraction:**
- Retrieves enrolled users from a specified Moodle course.
- Identifies learners using their assigned student role.
- Extracts relevant learner information, including names, email addresses and access timestamps.

**Activity data extraction:**
- Retrieves learner activity reports through a custom Moodle web service endpoint: `local_grades_get_activity_reports`.
- Extracts course, group, learner and activity information.
- Retrieves grades, due dates, submission dates and submission statuses.
- Retrieves activity modification timestamps to support incremental extraction.

### 2. Transformation

Pandas is used to clean and organise the extracted data into structured DataFrames.

The transformation process includes:

- Filtering learner records.
- Selecting relevant learner and activity information.
- Converting Moodle Unix timestamps into datetime values.
- Handling missing timestamp values.
- Converting numerical fields into appropriate data types.
- Adding extraction timestamps.
- Preparing records for database loading.

### 3. Data Quality Validation

Before loading data into PostgreSQL, the pipeline performs validation checks.

**Learner data validation:**
- Empty datasets.
- Missing learner IDs.
- Duplicate learner IDs.
- Missing first names and surnames.
- Missing email addresses.
- Invalid course counts.

**Activity report validation:**
- Empty datasets.
- Missing required identifiers.
- Duplicate activity record IDs.
- Invalid or missing required activity information.

The pipeline stops processing when validation fails and records the error in the pipeline execution history.

### 4. Loading

SQLAlchemy is used to connect to PostgreSQL and load the transformed learner and activity records.

The pipeline uses PostgreSQL UPSERT functionality to:

- Insert new learner and activity records.
- Update existing records when matching IDs already exist.
- Prevent duplicate records during repeated extractions.

Learner records use the Moodle user ID as their unique identifier, while activity records use their activity record IDs.

### 5. Incremental Extraction

The pipeline supports incremental extraction for Moodle activity reports.

Instead of retrieving all activity records during every run, it uses the modification timestamp of the last successful extraction.

The process works as follows:

1. Retrieve the last successful extraction timestamp from PostgreSQL.
2. Convert the timestamp into a Unix timestamp.
3. Apply a five-minute overlap to reduce the risk of missing records around extraction boundaries.
4. Pass the resulting timestamp to the Moodle API through the `since` parameter.
5. Retrieve new or modified activity records.
6. Transform, validate and load the returned records.
7. Update the extraction checkpoint after successful processing.

If no new or modified activity records are found, the pipeline skips activity transformation, validation and loading.

Learner data is currently retrieved and upserted on each pipeline run, while activity reporting uses incremental extraction.

### 6. Pipeline Execution Tracking

The pipeline maintains execution history and extraction checkpoints in PostgreSQL.

The `moodle_pipeline_run_history` table records:

- Pipeline run ID.
- Pipeline name.
- Start and completion timestamps.
- Number of records fetched.
- Number of records transformed.
- Number of records loaded.
- Pipeline execution status.
- Error messages when a run fails.

The `moodle_extraction_tracking` table stores the last successful extraction timestamp for incremental processing.

The pipeline also uses logging to capture execution progress, errors and processing results.

If an extraction, validation or loading operation fails, the pipeline records the failed run and does not advance the successful extraction checkpoint.

## Database Tables

The project currently uses four main tables:

**moodle_learners**

Stores transformed Moodle learner information, including learner IDs, names, email addresses, access timestamps and course counts.

**moodle_activity_reports**

Stores learner activity information, including course details, group information, activity types, grades, due dates, submission dates, modification timestamps and submission statuses.

**moodle_pipeline_run_history**

Stores pipeline execution history, including record counts, timestamps, execution status and error messages.

**moodle_extraction_tracking**

Stores the last successful extraction timestamp used to support incremental activity extraction.

## Example Pipeline Results

The following results were obtained during testing:

### Learner and activity extraction

| Metric | Result |
|---|---:|
| Moodle users retrieved | 80 |
| Learners transformed | 70 |
| Learner records loaded | 70 |
| Activity records retrieved | 80 |
| Activity records loaded | 80 |
| Learner validation | Passed |
| Activity validation | Passed |

### Incremental extraction and duplicate prevention

The pipeline was executed repeatedly to verify that:

- New or modified activity records could be retrieved using the `since` parameter.
- Existing records were updated through UPSERT operations.
- Repeated extraction did not create duplicate activity records.
- The activity table retained 80 records after reloading the same dataset.
- Duplicate activity IDs remained at zero.

### Failure handling

Controlled failure tests were performed to verify pipeline reliability.

| Test | Expected behaviour | Result |
|---|---|---|
| Moodle API failure | Record failed run and log error | Passed |
| PostgreSQL loading failure | Record failed run and log error | Passed |
| Checkpoint protection | Do not advance checkpoint after failure | Passed |
| Pipeline run tracking | Store failure status and error details | Passed |

These tests used simulated failures rather than actual infrastructure outages.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/maneliaugust/moodle_reporting_pipeline
cd moodle_reporting_pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add your Moodle API and PostgreSQL connection settings:

```env
MOODLE_URL=your_moodle_url
MOODLE_TOKEN=your_moodle_token

DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

Use your own configuration values. Never commit your API token or database credentials to GitHub.

### 5. Prepare the database

Ensure PostgreSQL is running and the reporting database exists.

The pipeline creates its required reporting tables when it starts.

### 6. Run the pipeline

```bash
python -m src.main
```

The pipeline will:

1. Connect to Moodle.
2. Extract learner data.
3. Retrieve new or modified activity reports.
4. Transform and validate the extracted data.
5. Load records into PostgreSQL.
6. Update pipeline execution history.
7. Update the extraction checkpoint after successful processing.

### 7. Supported Moodle Activities

The current activity reporting functionality supports three Moodle activity types:

- **Quizzes:** Retrieves learner quiz attempts, grades, submission dates and activity statuses.
- **Assignments:** Retrieves learner assignment submissions, grades, submission dates and activity statuses.
- **Forums:** Retrieves learner forum participation and related activity information.

Activity reports are retrieved from selected Moodle courses, groups and tagged activities through the custom Moodle web service.