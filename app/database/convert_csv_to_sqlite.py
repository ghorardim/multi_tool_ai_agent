import sqlite3
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_DIR = BASE_DIR / "datasets"
DATABASE_DIR = BASE_DIR / "app" / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Dataset Configuration
# --------------------------------------------------
DATASETS = [
    {
        "csv": "institutions.csv",
        "db": "institutions.db",
        "table": "institutions",
    },
    {
        "csv": "hospitals.csv",
        "db": "hospitals.db",
        "table": "hospitals",
    },
    {
        "csv": "restaurants.csv",
        "db": "restaurants.db",
        "table": "restaurants",
    },
]


# --------------------------------------------------
# Clean Column Names
# --------------------------------------------------
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names into SQL-friendly names.
    """

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace(r"[^\w]", "", regex=True)
    )

    return df


# --------------------------------------------------
# Convert CSV to SQLite
# --------------------------------------------------
def convert_csv_to_sqlite(csv_file, db_file, table_name):
    csv_path = DATASET_DIR / csv_file
    db_path = DATABASE_DIR / db_file

    if not csv_path.exists():
        print(f"\n❌ CSV not found: {csv_path}")
        return

    print("=" * 70)
    print(f"Reading: {csv_file}")

    df = pd.read_csv(csv_path)

    # Clean column names
    df = clean_column_names(df)

    # Print column names
    print("\nColumns:")
    for i, column in enumerate(df.columns, start=1):
        print(f"  {i}. {column}")

    # Print data types
    print("\nData Types:")
    print(df.dtypes)

    conn = sqlite3.connect(db_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    print(f"\n✅ Database Created : {db_file}")
    print(f"✅ Table            : {table_name}")
    print(f"✅ Total Rows       : {len(df)}")
    print(f"✅ Total Columns    : {len(df.columns)}")
    print()


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    print("\nConverting CSV files to SQLite databases...\n")

    for dataset in DATASETS:
        convert_csv_to_sqlite(
            dataset["csv"],
            dataset["db"],
            dataset["table"],
        )

    print("=" * 70)
    print("🎉 All databases created successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()