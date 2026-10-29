from pathlib import Path

import pandas as pd

from src.pump_etl import RAW_DATA_PATH, TIMESTAMP_COLUMN


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_PATH = REPORT_DIR / "pump_data_quality_report.txt"


def generate_report() -> str:
    """Generate a data quality report for the raw pump dataset."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    total_rows = len(df)
    total_columns = len(df.columns)
    total_cells = df.size
    missing_total = int(df.isna().sum().sum())

    timestamps = pd.to_datetime(
        df[TIMESTAMP_COLUMN],
        errors="coerce",
        utc=True,
    )

    invalid_timestamps = int(timestamps.isna().sum())
    valid_timestamps = timestamps.dropna()

    duplicate_rows = int(df.duplicated().sum())
    missing_by_column = df.isna().sum()

    lines = [
        "INDUSTRIAL DATA ENGINEERING",
        "PUMP SENSOR DATA QUALITY REPORT",
        "=" * 45,
        "",
        f"Source file: {RAW_DATA_PATH.name}",
        f"Total rows: {total_rows}",
        f"Total columns: {total_columns}",
        f"Total cells: {total_cells}",
        f"Missing cells: {missing_total}",
        (
            "Missing cell percentage: "
            f"{missing_total / total_cells * 100:.2f}%"
            if total_cells
            else "Missing cell percentage: N/A"
        ),
        f"Exact duplicate rows: {duplicate_rows}",
        f"Invalid timestamps: {invalid_timestamps}",
        "",
        "TIMESTAMP RANGE (UTC)",
        "-" * 45,
        (
            f"Start: {valid_timestamps.min()}"
            if not valid_timestamps.empty
            else "Start: N/A"
        ),
        (
            f"End: {valid_timestamps.max()}"
            if not valid_timestamps.empty
            else "End: N/A"
        ),
        "",
        "MISSING VALUES BY COLUMN",
        "-" * 45,
    ]

    for column, count in missing_by_column.items():
        percentage = count / total_rows * 100 if total_rows else 0
        lines.append(
            f"{column}: {count} ({percentage:.2f}%)"
        )

    report = "\n".join(lines)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nReport saved to: {REPORT_PATH}")

    return report


if __name__ == "__main__":
    generate_report()