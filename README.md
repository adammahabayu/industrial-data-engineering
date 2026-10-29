# Industrial Data Engineering Pipeline

A Python-based industrial data engineering project demonstrating ETL
(Extract, Transform, Load), data quality checks, CSV processing,
SQL analytics, SQLite storage, and automated testing.

The project includes two data pipelines:

1. A synthetic machine-sensor pipeline for demonstrating ETL logic
   and automated testing.
2. A centrifugal pump sensor pipeline that processes a publicly
   sourced dataset.

## Project Objectives

- Build reusable ETL pipelines with Python.
- Validate and clean timestamp and sensor data.
- Identify missing values and invalid timestamps.
- Store processed data in CSV and SQLite.
- Generate a data quality report.
- Perform basic SQL analytics on machine sensor readings.
- Test transformation logic using pytest.

## Project Structure

```text
industrial-data-engineering/
├── data/
│   ├── raw/
│   │   └── centrifugal_pump/
│   │       └── README.md
│   │       # Raw CSV is downloaded separately and Git-ignored
│   └── processed/
│       # Generated CSV and SQLite database; Git-ignored
├── reports/
│   └── pump_data_quality_report.txt
├── src/
│   ├── __init__.py
│   ├── etl.py
│   ├── pump_etl.py
│   ├── data_quality.py
│   └── analytics.py
├── tests/
│   └── test_etl.py
├── .gitignore
├── README.md
└── requirements.txt
```

Note: Generated files and directories may not appear in the Git
repository because they are excluded by `.gitignore`. The raw pump
CSV must be downloaded separately.

## Requirements

- Python 3.13
- pandas
- SQLAlchemy
- pytest

## Installation

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/adammahabayu/industrial-data-engineering.git
cd industrial-data-engineering
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Pipeline 1: Synthetic Sensor ETL

This pipeline uses generated sample data when its expected raw CSV
is unavailable. It demonstrates basic ETL behavior and is used by
the automated tests.

Run the pipeline:

```powershell
python -m src.etl
```

Expected outputs:

- `data/processed/machine_sensor_clean.csv`
- `data/processed/industrial_data.db`

SQLite table:

`machine_sensor_readings`

The synthetic data is intended for demonstration and testing.
It does not represent actual industrial sensor measurements.

## Pipeline 2: Centrifugal Pump Sensor ETL

### Dataset Source

The pump pipeline processes a CSV from the following public dataset
record:

- **Source:** [Centrifugal Pump Dataset on Zenodo](https://zenodo.org/records/18479728)
- **Local filename:** `A_2024-04-10.csv`
- **Local directory:** `data/raw/centrifugal_pump/`

Read `data/raw/centrifugal_pump/README.md` for dataset notes and
initial data quality audit results.

The raw CSV is excluded from Git. Download it from the original
source and place it at the expected path before running the pipeline.

Consult the original dataset record for authorship, dataset
description, license, and usage conditions.

### Run the Pipeline

```powershell
python -m src.pump_etl
```

The pipeline performs the following steps:

1. Reads the raw CSV file.
2. Converts timestamps to UTC.
3. Converts sensor columns to numeric values.
4. Removes rows with invalid timestamps.
5. Removes exact duplicate records.
6. Sorts records by timestamp.
7. Preserves missing sensor values for further data quality analysis.
8. Saves the processed data to CSV and SQLite.

Generated outputs:

- `data/processed/centrifugal_pump_clean.csv`
- `data/processed/industrial_data.db`

SQLite table:

`centrifugal_pump_readings`

The database is shared with the synthetic pipeline, but each pipeline
stores its data in a separate table.

## Data Quality Report

Generate a data quality report from the raw pump dataset:

```powershell
python -m src.data_quality
```

Output:

`reports/pump_data_quality_report.txt`

### Initial Dataset Audit

The raw CSV used during development contained the following:

| Metric | Result |
|---|---:|
| Rows | 4,981 |
| Columns | 11 |
| Missing cells | 271 |
| Missing cell percentage | 0.49% |
| Exact duplicate rows | 0 |
| Invalid timestamps | 1 |

Timestamp range (UTC):

- **Start:** `2024-04-10 12:00:00`
- **End:** `2024-04-10 13:59:59`

These figures describe the raw CSV audited during development.
The cleaned dataset contains 4,980 rows after the invalid timestamp
is removed.

Missing sensor values are preserved by the pump transformation
so that downstream analysis can determine an appropriate handling
strategy.

These checks do not establish that a pump has failed. The pipeline
does not infer failure labels or diagnose equipment faults.

## SQL Analytics

The project includes a basic SQL analytics module for summarizing
machine sensor readings from the synthetic pipeline.

Run the analytics module:

```powershell
python -m src.analytics
```

The module queries the `machine_sensor_readings` SQLite table and
generates a summary for each machine, including:

- Total sensor readings.
- Average temperature.
- Maximum vibration.
- Average pressure.

The results are calculated using SQL aggregation functions such as
`COUNT`, `AVG`, and `MAX`, grouped by machine ID.

**Scope:** This module currently analyzes the synthetic machine
sensor dataset. It does not yet analyze the centrifugal pump table.

## Automated Tests

Run the test suite:

```powershell
python -m pytest -v
```

The current test suite contains 11 tests covering:

- Missing-value handling in the synthetic pipeline.
- Duplicate removal and sorting.
- Required-column validation.
- CSV and SQLite output.
- UTC timestamp conversion in the pump pipeline.
- Invalid timestamp removal.
- Preservation of missing sensor values.
- Exact duplicate removal.
- Missing timestamp-column validation.

Latest development test result: **11 passed**.

Run the tests after modifying the ETL logic to check that existing
behavior remains correct.

## Current Limitations

- The pump pipeline processes a single downloaded CSV file.
- Missing sensor values are reported and preserved, not imputed.
- Sensor units and abnormal-value thresholds must be verified
  against the dataset documentation before interpreting readings.
- SQL analytics currently targets the synthetic machine sensor table.
- The project does not yet implement automated scheduling,
  production orchestration, or failure prediction.
- The pump pipeline does not currently include labeled failure
  events or a validated fault-detection model.

## Future Improvements

- Add structured logging and pipeline execution metadata.
- Extend SQL analytics to the centrifugal pump dataset.
- Add tests for database contents and data quality reports.
- Support configurable input files and larger datasets.
- Add reproducible dataset download instructions.
- Introduce automated pipeline scheduling and orchestration.
- Integrate with a predictive maintenance model when suitable
  labels and evaluation data are available.

## License and Dataset Attribution

The project code and the external dataset may be subject to
different license terms.

Review the original dataset record for its license, attribution
requirements, and permitted uses before redistributing the raw data.