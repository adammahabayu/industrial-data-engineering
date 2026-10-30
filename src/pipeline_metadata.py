from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "industrial_data.db"


def get_metadata_engine():
    """Create a database engine for pipeline metadata."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    return create_engine(
        f"sqlite:///{DATABASE_PATH.as_posix()}"
    )


def initialize_metadata_table() -> None:
    """Create the pipeline execution metadata table."""

    query = """
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            duration_seconds REAL,
            status TEXT NOT NULL,
            rows_input INTEGER,
            rows_output INTEGER,
            rows_removed INTEGER,
            error_message TEXT
        )
    """

    engine = get_metadata_engine()

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def start_pipeline_run(pipeline_name: str) -> dict:
    """Record the start of a pipeline execution."""

    initialize_metadata_table()

    start_time = datetime.now(timezone.utc)
    timer_start = perf_counter()

    query = """
        INSERT INTO pipeline_runs (
            pipeline_name,
            start_time,
            status
        )
        VALUES (
            :pipeline_name,
            :start_time,
            'RUNNING'
        )
    """

    engine = get_metadata_engine()

    try:
        with engine.begin() as connection:
            result = connection.execute(
                text(query),
                {
                    "pipeline_name": pipeline_name,
                    "start_time": start_time.isoformat(),
                },
            )

            run_id = result.lastrowid
    finally:
        engine.dispose()

    return {
        "run_id": run_id,
        "timer_start": timer_start,
    }


def finish_pipeline_run(
    run_id: int,
    timer_start: float,
    rows_input: int | None,
    rows_output: int | None,
    status: str = "SUCCESS",
    error_message: str | None = None,
) -> None:
    """Record the completion of a pipeline execution."""

    if status not in {"SUCCESS", "FAILED"}:
        raise ValueError("Status must be SUCCESS or FAILED")

    end_time = datetime.now(timezone.utc)
    duration = perf_counter() - timer_start

    rows_removed = None

    if rows_input is not None and rows_output is not None:
        rows_removed = rows_input - rows_output

    query = """
        UPDATE pipeline_runs
        SET
            end_time = :end_time,
            duration_seconds = :duration,
            status = :status,
            rows_input = :rows_input,
            rows_output = :rows_output,
            rows_removed = :rows_removed,
            error_message = :error_message
        WHERE id = :run_id
    """

    engine = get_metadata_engine()

    try:
        with engine.begin() as connection:
            connection.execute(
                text(query),
                {
                    "run_id": run_id,
                    "end_time": end_time.isoformat(),
                    "duration": round(duration, 4),
                    "status": status,
                    "rows_input": rows_input,
                    "rows_output": rows_output,
                    "rows_removed": rows_removed,
                    "error_message": error_message,
                },
            )
    finally:
        engine.dispose()