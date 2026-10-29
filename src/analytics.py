from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "industrial_data.db"


def get_engine():
    """Create a SQLAlchemy engine for the project database."""
    return create_engine(f"sqlite:///{DATABASE_PATH.as_posix()}")


def get_machine_summary() -> pd.DataFrame:
    """Summarize sensor readings from the synthetic dataset."""
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


def get_pump_summary() -> pd.DataFrame:
    """Summarize sensor readings from the centrifugal pump dataset."""
    query = """
        SELECT
            COUNT(*) AS total_readings,
            MIN("Timestamp") AS first_reading_utc,
            MAX("Timestamp") AS last_reading_utc,

            ROUND(AVG("A_Pres.PV"), 3) AS avg_pressure,
            ROUND(MIN("A_Pres.PV"), 3) AS min_pressure,
            ROUND(MAX("A_Pres.PV"), 3) AS max_pressure,

            ROUND(AVG("A_Temp.PV"), 3) AS avg_pump_temperature,
            ROUND(MIN("A_Temp.PV"), 3) AS min_pump_temperature,
            ROUND(MAX("A_Temp.PV"), 3) AS max_pump_temperature,

            SUM(
                CASE WHEN "A_Pres.PV" IS NULL
                THEN 1 ELSE 0 END
            ) AS missing_pressure,

            SUM(
                CASE WHEN "A_Temp.PV" IS NULL
                THEN 1 ELSE 0 END
            ) AS missing_pump_temperature,

            SUM(
                CASE WHEN "A_ACR_Mot.PV" IS NULL
                THEN 1 ELSE 0 END
            ) AS missing_motor_readings,

            SUM(
                CASE WHEN "A_ACR_Pmp.PV" IS NULL
                THEN 1 ELSE 0 END
            ) AS missing_pump_readings

        FROM centrifugal_pump_readings
    """

    engine = get_engine()

    try:
        with engine.connect() as connection:
            return pd.read_sql_query(query, connection)
    finally:
        engine.dispose()


if __name__ == "__main__":
    print("=" * 60)
    print("SYNTHETIC MACHINE SENSOR ANALYTICS")
    print("=" * 60)

    print(get_machine_summary().to_string(index=False))

    print("\n" + "=" * 60)
    print("CENTRIFUGAL PUMP SENSOR ANALYTICS")
    print("=" * 60)

    print(get_pump_summary().to_string(index=False))