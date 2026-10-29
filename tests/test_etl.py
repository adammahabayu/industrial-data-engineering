import pandas as pd
import pytest
import src.etl as etl

from src.etl import REQUIRED_COLUMNS, create_sample_data, transform
from sqlalchemy import create_engine, inspect
from src.pump_etl import transform as transform_pump


def test_transform_removes_missing_values():
    raw_df = create_sample_data()

    clean_df = transform(raw_df)

    assert clean_df.isna().sum().sum() == 0
    assert len(clean_df) == 5


def test_transform_removes_duplicates():
    raw_df = create_sample_data()

    clean_df = transform(raw_df)

    assert not clean_df.duplicated().any()


def test_transform_sorts_by_machine_and_timestamp():
    raw_df = create_sample_data()

    clean_df = transform(raw_df)

    for _, group in clean_df.groupby("machine_id"):
        assert group["timestamp"].is_monotonic_increasing


def test_transform_rejects_missing_columns():
    raw_df = create_sample_data()
    raw_df = raw_df.drop(columns=["temperature"])

    with pytest.raises(ValueError, match="Missing required columns"):
        transform(raw_df)


def test_transform_keeps_required_columns():
    raw_df = create_sample_data()

    clean_df = transform(raw_df)

    assert list(clean_df.columns) == REQUIRED_COLUMNS

def test_load_saves_csv_and_sqlite(tmp_path, monkeypatch):
    csv_path = tmp_path / "machine_sensor_clean.csv"
    db_path = tmp_path / "industrial_data.db"

    monkeypatch.setattr(etl, "PROCESSED_DATA_PATH", csv_path)
    monkeypatch.setattr(etl, "DATABASE_PATH", db_path)

    clean_df = etl.transform(etl.create_sample_data())

    etl.load(clean_df)

    # Pastikan file CSV berhasil dibuat.
    assert csv_path.exists()

    saved_csv = pd.read_csv(csv_path)
    assert len(saved_csv) == len(clean_df)

    # Pastikan database SQLite dan tabel berhasil dibuat.
    assert db_path.exists()

    engine = create_engine(f"sqlite:///{db_path.as_posix()}")
    try:
        assert inspect(engine).has_table("machine_sensor_readings")

        saved_db = pd.read_sql(
            "SELECT * FROM machine_sensor_readings",
            engine,
        )
        assert len(saved_db) == len(clean_df)
    finally:
        engine.dispose()

def test_pump_transform_converts_timestamp_to_utc():
    raw_df = pd.DataFrame(
        {
            "Timestamp": ["2024-04-10T12:00:00Z"],
            "A_Pres.PV": [0.45],
        }
    )

    clean_df = transform_pump(raw_df)

    assert pd.api.types.is_datetime64_any_dtype(
        clean_df["Timestamp"]
    )
    assert str(clean_df["Timestamp"].dt.tz) == "UTC"

def test_pump_transform_removes_invalid_timestamp():
    raw_df = pd.DataFrame(
        {
            "Timestamp": [
                "2024-04-10T12:00:00Z",
                "invalid-timestamp",
            ],
            "A_Pres.PV": [0.45, 0.50],
        }
    )

    clean_df = transform_pump(raw_df)

    assert len(clean_df) == 1


def test_pump_transform_preserves_missing_sensor_values():
    raw_df = pd.DataFrame(
        {
            "Timestamp": ["2024-04-10T12:00:00Z"],
            "A_Pres.PV": [None],
        }
    )

    clean_df = transform_pump(raw_df)

    assert len(clean_df) == 1
    assert pd.isna(clean_df.loc[0, "A_Pres.PV"])


def test_pump_transform_removes_exact_duplicates():
    raw_df = pd.DataFrame(
        {
            "Timestamp": [
                "2024-04-10T12:00:00Z",
                "2024-04-10T12:00:00Z",
            ],
            "A_Pres.PV": [0.45, 0.45],
        }
    )

    clean_df = transform_pump(raw_df)

    assert len(clean_df) == 1


def test_pump_transform_rejects_missing_timestamp_column():
    raw_df = pd.DataFrame(
        {
            "A_Pres.PV": [0.45],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required column",
    ):
        transform_pump(raw_df)