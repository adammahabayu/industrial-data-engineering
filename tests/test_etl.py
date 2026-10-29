import pandas as pd
import pytest
import src.etl as etl

from src.etl import REQUIRED_COLUMNS, create_sample_data, transform
from sqlalchemy import create_engine, inspect


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