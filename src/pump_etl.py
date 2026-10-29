from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


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
    """Run the pump sensor ETL pipeline."""

    raw_df = extract()
    clean_df = transform(raw_df)

    load(clean_df)

    print(f"Source file: {RAW_DATA_PATH.name}")
    print(f"Raw rows: {len(raw_df)}")
    print(f"Clean rows: {len(clean_df)}")
    print(
        f"Rows removed: {len(raw_df) - len(clean_df)}"
    )
    print(
        "Missing values before cleaning:",
        int(raw_df.isna().sum().sum()),
    )
    print(
        "Missing values after cleaning:",
        int(clean_df.isna().sum().sum()),
    )
    print(
        f"Clean CSV: {PROCESSED_CSV_PATH}"
    )
    print(
        f"SQLite database: {DATABASE_PATH}"
    )
    print(f"SQLite table: {TABLE_NAME}")

    return clean_df


if __name__ == "__main__":
    run_pipeline()