# Centrifugal Pump Dataset

## Source

- Dataset: Centrifugal Pump Dataset
- Source URL: https://zenodo.org/records/18479728
- Local filename: `A_2024-04-10.csv`

Please refer to the original Zenodo record for the dataset's
full description, authorship, license, and usage conditions.

## Local Dataset

The raw CSV is stored locally at:

`data/raw/centrifugal_pump/A_2024-04-10.csv`

The raw data file is excluded from Git using `.gitignore`.
Download the dataset from the original source before running
the pump ETL pipeline.

## Initial Data Audit

- Rows: 4,981
- Columns: 11
- Missing cells: 271
- Invalid timestamps: 1
- Exact duplicate rows: 0
- Timestamp range (UTC):
  `2024-04-10 12:00:00` to `2024-04-10 13:59:59`

These figures describe the downloaded CSV used in this project.

## Data Handling

The pipeline:

1. Converts timestamps to UTC.
2. Converts sensor fields to numeric values.
3. Removes rows with invalid timestamps.
4. Removes exact duplicate rows.
5. Sorts records by timestamp.
6. Preserves missing sensor values for data-quality analysis.

The project does not infer equipment failures or assign fault labels
unless supported by documented labels in the source dataset.