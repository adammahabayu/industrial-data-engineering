from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from src.logging_config import setup_logging
from src.pipeline_metadata import (
    finish_pipeline_run,
    start_pipeline_run,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "machine_sensor_data.csv"
PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "machine_sensor_clean.csv"
)
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "industrial_data.db"

REQUIRED_COLUMNS = [
    "timestamp",
    "machine_id",
    "temperature",
    "vibration",
    "pressure",
]

logger = setup_logging()


def create_sample_data() -> pd.DataFrame:
    """Create sample industrial sensor data for ETL development."""
    return pd.DataFrame(
        [
            ["2026-10-29 08:00:00", "M001", 72.5, 0.12, 101.3],
            ["2026-10-29 08:05:00", "M001", 73.1, 0.13, 101.1],
            ["2026-10-29 08:10:00", "M001", None, 0.14, 100.9],
            ["2026-10-29 08:15:00", "M002", 68.4, 0.10, 102.0],
            ["2026-10-29 08:20:00", "M002", 69.0, 0.11, 101.8],
            ["2026-10-29 08:20:00", "M002", 69.0, 0.11, 101.8],
            ["2026-10-29 08:25:00", "M003", 75.2, 0.20, 99.8],
        ],
        columns=REQUIRED_COLUMNS,
    )


def extract() -> pd.DataFrame:
    """Extract raw data from CSV, creating sample data if needed."""
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not RAW_DATA_PATH.exists():
        create_sample_data().to_csv(RAW_DATA_PATH, index=False)

    return pd.read_csv(RAW_DATA_PATH)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Validate, clean, and transform raw sensor data."""
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    clean_df = df[REQUIRED_COLUMNS].copy()

    clean_df["timestamp"] = pd.to_datetime(
        clean_df["timestamp"],
        errors="coerce",
    )

    clean_df["machine_id"] = (
        clean_df["machine_id"].astype("string").str.strip()
    )

    numeric_columns = ["temperature", "vibration", "pressure"]

    for column in numeric_columns:
        clean_df[column] = pd.to_numeric(
            clean_df[column],
            errors="coerce",
        )

    clean_df = clean_df.dropna(subset=REQUIRED_COLUMNS)
    clean_df = clean_df.drop_duplicates()
    clean_df = clean_df[clean_df["machine_id"] != ""]

    clean_df = clean_df.sort_values(
        ["machine_id", "timestamp"]
    ).reset_index(drop=True)

    return clean_df


def load(df: pd.DataFrame) -> None:
    """Load transformed data into CSV and SQLite."""
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_DATA_PATH, index=False)

    engine = create_engine(
        f"sqlite:///{DATABASE_PATH.as_posix()}"
    )

    try:
        df.to_sql(
            "machine_sensor_readings",
            engine,
            if_exists="replace",
            index=False,
        )
    finally:
        engine.dispose()


def run_pipeline() -> pd.DataFrame:
    """Execute the full ETL pipeline with logging and metadata tracking."""

    pipeline_name = "machine_sensor_etl"

    run = start_pipeline_run(pipeline_name)

    run_id = run["run_id"]
    timer_start = run["timer_start"]

    raw_df = None
    clean_df = None

    logger.info(
        "Starting pipeline: %s | Run ID: %s",
        pipeline_name,
        run_id,
    )

    try:
        logger.info("Extracting raw sensor data...")
        raw_df = extract()

        logger.info(
            "Extraction completed. Rows: %s",
            len(raw_df),
        )

        logger.info("Transforming sensor data...")
        clean_df = transform(raw_df)

        logger.info(
            "Transformation completed. Rows: %s",
            len(clean_df),
        )

        logger.info("Loading processed data...")
        load(clean_df)

    except Exception as exc:
        finish_pipeline_run(
            run_id=run_id,
            timer_start=timer_start,
            rows_input=len(raw_df) if raw_df is not None else None,
            rows_output=len(clean_df) if clean_df is not None else None,
            status="FAILED",
            error_message=str(exc),
        )

        logger.exception(
            "Pipeline failed: %s | Run ID: %s",
            pipeline_name,
            run_id,
        )

        raise

    finish_pipeline_run(
        run_id=run_id,
        timer_start=timer_start,
        rows_input=len(raw_df),
        rows_output=len(clean_df),
        status="SUCCESS",
    )

    logger.info(
        "Pipeline completed successfully: %s | Run ID: %s",
        pipeline_name,
        run_id,
    )
    logger.info("Raw rows: %s", len(raw_df))
    logger.info("Clean rows: %s", len(clean_df))
    logger.info("Rows removed: %s", len(raw_df) - len(clean_df))
    logger.info("CSV output: %s", PROCESSED_DATA_PATH)
    logger.info("SQLite database: %s", DATABASE_PATH)

    return clean_df


if __name__ == "__main__":
    run_pipeline()