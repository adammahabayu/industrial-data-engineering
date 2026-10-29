from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "industrial_data.db"


def get_engine():
    """Create a SQLAlchemy engine for the project database."""
    return create_engine(f"sqlite:///{DATABASE_PATH.as_posix()}")


def get_machine_summary() -> pd.DataFrame:
    """Summarize sensor readings for each machine."""
    query = """
        SELECT
            machine_id,
            COUNT(*) AS total_readings,
            ROUND(AVG(temperature), 2) AS avg_temperature,
            ROUND(MAX(vibration), 3) AS max_vibration,
            ROUND(AVG(pressure), 2) AS avg_pressure
        FROM machine_sensor_readings
        GROUP BY machine_id
        ORDER BY machine_id
    """

    engine = get_engine()
    try:
        with engine.connect() as connection:
            return pd.read_sql_query(query, connection)
    finally:
        engine.dispose()


if __name__ == "__main__":
    summary = get_machine_summary()
    print(summary.to_string(index=False))