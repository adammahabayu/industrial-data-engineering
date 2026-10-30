from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from src.logging_config import setup_logging
from src.pipeline_metadata import (
    finish_pipeline_run,
    start_pipeline_run,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "centrifugal_pump"
    / "A_2024-04-10.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_CSV_PATH = (
    PROCESSED_DIR / "centrifugal_pump_clean.csv"
)

DATABASE_PATH = (
    PROCESSED_DIR / "industrial_data.db"
)

TABLE_NAME = "centrifugal_pump_readings"

TIMESTAMP_COLUMN = "Timestamp"

logger = setup_logging()


def extract() -> pd.DataFrame:
    """Read the original pump sensor CSV."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    return pd.read_csv(RAW_DATA_PATH)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean pump sensor data."""

    if TIMESTAMP_COLUMN not in df.columns:
        raise ValueError(
            f"Missing required column: {TIMESTAMP_COLUMN}"
        )

    clean_df = df.copy()

    clean_df[TIMESTAMP_COLUMN] = pd.to_datetime(
        clean_df[TIMESTAMP_COLUMN],
        errors="coerce",
        utc=True,
    )

    numeric_columns = [
        column
        for column in clean_df.columns
        if column != TIMESTAMP_COLUMN
    ]

    for column in numeric_columns:
        clean_df[column] = pd.to_numeric(
            clean_df[column],
            errors="coerce",
        )

    # A timestamp is required to identify when a reading occurred.
    # Sensor values may remain missing for data-quality analysis.
    clean_df = clean_df.dropna(
        subset=[TIMESTAMP_COLUMN]
    )

    # Remove exact duplicate records only.
    clean_df = clean_df.drop_duplicates()

    clean_df = clean_df.sort_values(
        TIMESTAMP_COLUMN
    ).reset_index(drop=True)

    return clean_df


def load(df: pd.DataFrame) -> None:
    """Save cleaned data to CSV and SQLite."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_CSV_PATH,
        index=False,
    )

    engine = create_engine(
        f"sqlite:///{DATABASE_PATH.as_posix()}"
    )

    try:
        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists="replace",
            index=False,
        )
    finally:
        engine.dispose()


def run_pipeline() -> pd.DataFrame:
    """Run the pump sensor ETL pipeline with logging and metadata."""

    pipeline_name = "centrifugal_pump_etl"

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
        logger.info(
            "Extracting pump sensor data from %s...",
            RAW_DATA_PATH.name,
        )

        raw_df = extract()

        logger.info(
            "Extraction completed. Rows: %s",
            len(raw_df),
        )

        logger.info("Transforming pump sensor data...")

        clean_df = transform(raw_df)

        logger.info(
            "Transformation completed. Rows: %s",
            len(clean_df),
        )

        logger.info("Loading processed pump data...")

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

    logger.info("Source file: %s", RAW_DATA_PATH.name)
    logger.info("Raw rows: %s", len(raw_df))
    logger.info("Clean rows: %s", len(clean_df))
    logger.info(
        "Rows removed: %s",
        len(raw_df) - len(clean_df),
    )

    logger.info(
        "Missing values before cleaning: %s",
        int(raw_df.isna().sum().sum()),
    )

    logger.info(
        "Missing values after cleaning: %s",
        int(clean_df.isna().sum().sum()),
    )

    logger.info("Clean CSV: %s", PROCESSED_CSV_PATH)
    logger.info("SQLite database: %s", DATABASE_PATH)
    logger.info("SQLite table: %s", TABLE_NAME)

    return clean_df


if __name__ == "__main__":
    run_pipeline()