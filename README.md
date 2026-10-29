# Industrial Data Engineering Pipeline

A simple industrial data engineering project that processes machine
sensor readings using an Extract, Transform, Load (ETL) pipeline.

## Project Overview

This project demonstrates a basic data pipeline for industrial sensor
data, including data extraction, cleaning, validation, deduplication,
and loading into CSV and SQLite.

The sample dataset contains machine sensor readings with the following
attributes:

- Timestamp
- Machine ID
- Temperature
- Vibration
- Pressure

## Pipeline Architecture

Raw CSV Data
    |
    v
Extract
    |
    v
Transform
    - Validate required columns
    - Convert data types
    - Remove missing values
    - Remove duplicate records
    - Sort by machine and timestamp
    |
    v
Load
    - Clean CSV
    - SQLite database

## Project Structure

industrial-data-engineering/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   └── etl.py
├── tests/
│   └── test_etl.py
├── .gitignore
├── README.md
└── requirements.txt

## Requirements

- Python 3.13
- pandas
- SQLAlchemy
- pytest

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

    python -m venv .venv

Activate it on Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements.txt

## Run the Pipeline

Run the ETL pipeline:

    python -m src.etl

If the raw CSV does not exist, the pipeline generates sample data
automatically.

The pipeline creates:

- data/processed/machine_sensor_clean.csv
- data/processed/industrial_data.db

The SQLite database contains the table:

    machine_sensor_readings

## Run Tests

Run the automated tests:

    python -m pytest tests/test_etl.py -v

The tests cover data cleaning, duplicate removal, sorting, required
column validation, and CSV/SQLite output.

## Current Results

Using the built-in sample dataset:

- Raw records: 7
- Clean records: 5
- Removed records: 2
- Automated tests: 6 passed

## Future Improvements

- Integrate a larger real-world industrial dataset.
- Add data quality reports and logging.
- Add SQL-based analytical queries.
- Schedule automated pipeline execution.
- Integrate the pipeline with a predictive maintenance model.