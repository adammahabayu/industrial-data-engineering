# Industrial Data Engineering Pipeline

A Python-based industrial data engineering project demonstrating ETL (Extract, Transform, Load), data quality checks, CSV processing, SQL analytics, SQLite storage, structured logging, pipeline execution metadata, automated testing, and interactive dashboard monitoring.

The project includes two data pipelines:

1. A synthetic machine-sensor pipeline for demonstrating ETL logic and automated testing.
2. A centrifugal pump sensor pipeline that processes a publicly sourced industrial dataset.

## Project Objectives

- Build reusable ETL pipelines with Python.
- Validate and clean timestamps and sensor data.
- Identify missing values and invalid timestamps.
- Store processed data in CSV and SQLite.
- Generate data quality reports.
- Perform SQL analytics on industrial sensor data.
- Implement structured logging for pipeline execution.
- Track pipeline execution metadata in SQLite.
- Build an interactive dashboard using Streamlit and Plotly.
- Test transformation and analytics logic using pytest.

## Project Structure

```text
industrial-data-engineering/
├── dashboard/
│   ├── app.py
│   ├── components.py
│   ├── database.py
│   └── views/
│       ├── overview.py
│       ├── pipeline_monitoring.py
│       ├── sensor_analytics.py
│       └── data_quality.py
├── data/
│   ├── raw/
│   │   └── centrifugal_pump/
│   │       └── README.md
│   └── processed/
├── logs/
├── reports/
├── src/
│   ├── etl.py
│   ├── pump_etl.py
│   ├── data_quality.py
│   ├── analytics.py
│   ├── logging_config.py
│   └── pipeline_metadata.py
├── tests/
│   └── test_etl.py
├── .gitignore
├── README.md
└── requirements.txt