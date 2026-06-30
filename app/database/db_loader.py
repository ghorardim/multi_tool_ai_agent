from pathlib import Path

from langchain_community.utilities import SQLDatabase

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database directory
DATABASE_DIR = BASE_DIR / "app" / "database"


def get_database(db_name: str) -> SQLDatabase:
    """
    Returns a SQLDatabase object for the given SQLite database.

    Example:
        db = get_database("hospitals.db")
    """

    db_path = DATABASE_DIR / db_name

    if not db_path.exists():
        raise FileNotFoundError(
            f"Database '{db_name}' does not exist.\n"
            f"Expected location: {db_path}"
        )

    return SQLDatabase.from_uri(f"sqlite:///{db_path}")