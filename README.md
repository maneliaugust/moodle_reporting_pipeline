# Moodle Reporting Pipeline – Python & PostgreSQL

## Project Overview

This project is an automated ETL (Extract, Transform, Load) pipeline that retrieves learner data from a Moodle Learning Management System (LMS) using the Moodle REST API.

The pipeline uses Python and Pandas to extract, clean, transform and validate learner data before storing it in a PostgreSQL database.

It also includes data quality checks, UPSERT functionality and pipeline execution tracking to support reliable reporting and future data analysis.

## Technologies Used

- **Python** – ETL development and API integration
- **Moodle REST API** – Data extraction
- **Pandas** – Data transformation and cleaning
- **PostgreSQL** – Data storage
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
│   └── tracking.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ETL Pipeline Process

### 1. Extraction

The pipeline connects to Moodle through its REST API to retrieve course and enrolled-user information.

The current implementation retrieves enrolled users from a specified Moodle course and identifies learners using their assigned student role.

### 2. Transformation

Pandas is used to:

- Filter learner records.
- Select relevant learner information.
- Organise data into a structured DataFrame.
- Convert Moodle timestamps into datetime values.
- Handle missing timestamp values.
- Add an extraction timestamp.

### 3. Data Quality Validation

Before loading data into PostgreSQL, the pipeline checks for:

- Empty datasets.
- Missing learner IDs.
- Duplicate learner IDs.
- Missing first names and surnames.
- Missing email addresses.
- Invalid course counts.

The pipeline stops if validation fails.

### 4. Loading

SQLAlchemy is used to connect to PostgreSQL and load the transformed learner records.

The pipeline uses an UPSERT operation to insert new learners and update existing records using the Moodle user ID as the unique identifier.

This prevents duplicate learner records when the pipeline runs multiple times.

### 5. Pipeline Execution Tracking

The pipeline maintains a `moodle_pipeline_run_history` table in PostgreSQL.

It records:

- Pipeline run ID.
- Pipeline name.
- Start and completion timestamps.
- Number of records fetched.
- Number of records transformed.
- Number of records loaded.
- Pipeline execution status.
- Error messages when a run fails.

## Database Tables

The project currently uses two main tables:

**moodle_learners**

Stores the transformed Moodle learner information, including learner IDs, names, email addresses, access timestamps and course counts.

**moodle_pipeline_run_history**

Stores pipeline execution history, including record counts, timestamps and execution status.

## Example Pipeline Results

A successful pipeline execution returned the following results:

| Metric | Result |
|---|---:|
| Moodle users retrieved | 80 |
| Learners transformed | 70 |
| Data quality validation | Passed |
| Learner records loaded | 70 |
| Pipeline status | Success |

The pipeline was also executed more than once to verify that the UPSERT functionality prevents duplicate learner records.

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
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

### 5. Run the pipeline

```bash
python -m src.main
```

The pipeline will create the required database tables if they do not already exist, retrieve Moodle learner data, transform and validate the records, load them into PostgreSQL and update the execution history.
