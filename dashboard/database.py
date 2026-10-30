from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "industrial_data.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


def get_engine():
    """Create a SQLAlchemy engine for the project database."""

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    return create_engine(DATABASE_URL)


def get_pipeline_history() -> pd.DataFrame:
    """Retrieve pipeline execution history."""

    query = """
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
        ORDER BY id DESC
    """

    engine = get_engine()

    try:
        with engine.connect() as connection:
            return pd.read_sql_query(
                text(query),
                connection,
            )
    finally:
        engine.dispose()


def get_machine_sensor_data() -> pd.DataFrame:
    """Retrieve cleaned machine sensor data."""

    query = """
        SELECT *
        FROM machine_sensor_readings
        ORDER BY timestamp
    """

    engine = get_engine()

    try:
        with engine.connect() as connection:
            return pd.read_sql_query(
                text(query),
                connection,
            )
    finally:
        engine.dispose()


def get_pump_sensor_data() -> pd.DataFrame:
    """Retrieve cleaned centrifugal pump sensor data."""

    query = """
        SELECT *
        FROM centrifugal_pump_readings
        ORDER BY Timestamp
    """

    engine = get_engine()

    try:
        with engine.connect() as connection:
            return pd.read_sql_query(
                text(query),
                connection,
            )
    finally:
        engine.dispose()


def get_database_summary() -> dict:
    """Retrieve basic database statistics."""

    engine = get_engine()

    queries = {
        "pipeline_runs": """
            SELECT COUNT(*) AS total
            FROM pipeline_runs
        """,
        "machine_sensor_readings": """
            SELECT COUNT(*) AS total
            FROM machine_sensor_readings
        """,
        "centrifugal_pump_readings": """
            SELECT COUNT(*) AS total
            FROM centrifugal_pump_readings
        """,
        "successful_runs": """
            SELECT COUNT(*) AS total
            FROM pipeline_runs
            WHERE status = 'SUCCESS'
        """,
        "failed_runs": """
            SELECT COUNT(*) AS total
            FROM pipeline_runs
            WHERE status = 'FAILED'
        """,
    }

    summary = {}

    try:
        with engine.connect() as connection:
            for key, query in queries.items():
                result = connection.execute(
                    text(query)
                ).scalar()

                summary[key] = result or 0

    finally:
        engine.dispose()

    return summary