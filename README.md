# Industrial Data Engineering Pipeline

A Python-based industrial data engineering project demonstrating ETL (Extract, Transform, Load), data quality checks, CSV processing, SQL analytics, SQLite storage, structured logging, pipeline execution metadata, and automated testing.

The project includes two data pipelines:

1. A synthetic machine-sensor pipeline for demonstrating ETL logic and automated testing.
2. A centrifugal pump sensor pipeline that processes a publicly sourced industrial dataset.

## Project Objectives

- Build reusable ETL pipelines with Python.
- Validate and clean timestamps and sensor data.
- Identify missing values and invalid timestamps.
- Store processed data in CSV and SQLite.
- Generate a data quality report.
- Perform SQL analytics on synthetic machine and pump sensor data.
- Implement structured logging for pipeline execution.
- Track pipeline execution metadata in SQLite.
- Test transformation and analytics logic using pytest.

## Project Structure

```text
industrial-data-engineering/
|-- data/
|   |-- raw/
|   |   |-- centrifugal_pump/
|   |       |-- README.md
|   |       # Raw CSV is downloaded separately and Git-ignored
|   |-- processed/
|       # Generated CSV and SQLite database; Git-ignored
|-- logs/
|   # Generated pipeline logs; Git-ignored
|-- reports/
|   |-- README.md
|   # Generated data quality report; Git-ignored
|-- src/
|   |-- __init__.py
|   |-- etl.py
|   |-- pump_etl.py
|   |-- data_quality.py
|   |-- analytics.py
|   |-- logging_config.py
|   |-- pipeline_metadata.py
|-- tests/
|   |-- test_etl.py
|-- .gitignore
|-- README.md
|-- requirements.txt
```

## Requirements

- Python 3.10 or later
- pip
- Git
- SQLite

Python dependencies are listed in `requirements.txt`.

## Installation and Setup

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/adammahabayu/industrial-data-engineering.git
cd industrial-data-engineering
```

If you already have the project folder, you can skip this step.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Download the Centrifugal Pump Dataset

Download the dataset from:

https://zenodo.org/records/18479728

Place `A_2024-04-10.csv` inside:

`data/raw/centrifugal_pump/`

The raw dataset is not included in this repository and must be downloaded separately.

## Running the Pipelines

This project contains two independent ETL pipelines.

### 1. Machine Sensor Pipeline

Run:

```bash
python -m src.etl
```

This pipeline:

- Extracts machine sensor data from CSV.
- Validates required columns.
- Converts timestamps and sensor values.
- Handles missing and duplicate records.
- Saves cleaned data to CSV and SQLite.
- Records execution logs and pipeline metadata.

Output:

- CSV: `data/processed/machine_sensor_clean.csv`
- SQLite table: `machine_sensor_readings`

### 2. Centrifugal Pump Pipeline

Run:

```bash
python -m src.pump_etl
```

This pipeline:

- Extracts centrifugal pump sensor data.
- Validates and converts timestamps.
- Converts sensor columns to numeric values.
- Removes invalid timestamps and duplicate records.
- Preserves missing sensor values for data quality analysis.
- Saves cleaned data to CSV and SQLite.
- Records execution logs and pipeline metadata.

Output:

- CSV: `data/processed/centrifugal_pump_clean.csv`
- SQLite table: `centrifugal_pump_readings`

Both pipelines store their data in:

`data/processed/industrial_data.db`

## Data Quality Report

The project includes data quality checks for the centrifugal pump dataset.

The checks cover:

- Total number of rows and columns.
- Missing values.
- Invalid timestamps.
- Duplicate records.
- Dataset observation time range.

### Dataset Summary

| Metric | Result |
|---|---:|
| Original rows | 4,981 |
| Rows after cleaning | 4,980 |
| Missing values before cleaning | 271 |
| Missing values after cleaning | 260 |
| Invalid timestamps | 1 |
| Duplicate rows | 0 |

Missing sensor values are intentionally preserved after cleaning so they remain available for data quality analysis.

The generated report is stored at:

`reports/pump_data_quality_report.txt`

## SQL Analytics

SQLite is used to store processed sensor data and perform analytical queries.

The analytics module supports:

- Sensor reading summaries.
- Average, minimum, and maximum sensor values.
- Missing value analysis.
- Dataset observation time range.
- Machine and pump sensor data analysis.

Database location:

`data/processed/industrial_data.db`

## Structured Logging

The project uses Python's built-in logging module to record pipeline execution activities.

The logging system records:

- Pipeline execution timestamps.
- Extract, transform, and load activities.
- Number of input and output records.
- Number of removed records.
- Output file locations.
- Pipeline execution status.
- Error details when a pipeline fails.

Logs are written to:

`logs/pipeline.log`

Log messages are also displayed directly in the terminal during pipeline execution.

## Pipeline Execution Metadata

Each pipeline execution is recorded in the `pipeline_runs` table inside the SQLite database.

The metadata includes:

| Column | Description |
|---|---|
| `id` | Unique execution ID |
| `pipeline_name` | Name of the executed pipeline |
| `start_time` | Pipeline start timestamp |
| `end_time` | Pipeline completion timestamp |
| `duration_seconds` | Pipeline execution duration |
| `status` | Pipeline execution status |
| `rows_input` | Number of input records |
| `rows_output` | Number of output records |
| `rows_removed` | Number of removed records |
| `error_message` | Error details if execution fails |

Pipeline execution statuses:

- `RUNNING`: The pipeline is currently executing.
- `SUCCESS`: The pipeline completed successfully.
- `FAILED`: The pipeline execution failed.

This feature provides execution history and basic monitoring for both ETL pipelines.

### Viewing Pipeline Execution History

The execution history can be queried using SQL:

```sql
SELECT
    id,
    pipeline_name,
    start_time,
    end_time,
    duration_seconds,
    status,
    rows_input,
    rows_output,
    rows_removed,
    error_message
FROM pipeline_runs
ORDER BY id DESC;
```

## Automated Tests

The project uses pytest to validate ETL transformations and analytics logic.

Run the test suite:

```bash
python -m pytest -v
```

Latest test results:

- Total tests: 14
- Passed: 14
- Failed: 0

The automated tests cover:

- Machine sensor data cleaning.
- Required column validation.
- Missing value handling.
- Duplicate record removal.
- Timestamp transformation.
- CSV and SQLite data loading.
- Pump sensor data cleaning.
- Pump analytics and summary calculations.

## Current Limitations

- Synthetic machine sensor data is currently generated for development and testing.
- The centrifugal pump pipeline currently processes one dataset file.
- No interactive monitoring dashboard is available.
- Pipeline orchestration is not yet automated.
- Dedicated automated tests for logging and pipeline metadata have not yet been implemented.

## Future Improvements

Potential improvements include:

- Integrating additional industrial sensor datasets.
- Building an interactive monitoring dashboard using Streamlit.
- Implementing pipeline orchestration using Apache Airflow.
- Adding notifications for failed pipeline executions.
- Expanding automated tests for logging and pipeline metadata.
- Developing predictive analytics for machine condition monitoring.

## License and Dataset Attribution

This project was developed for educational and portfolio purposes in the field of Data Engineering.

The centrifugal pump dataset was obtained from Zenodo:

https://zenodo.org/records/18479728

Dataset usage is subject to the license and attribution requirements specified by the dataset provider.
