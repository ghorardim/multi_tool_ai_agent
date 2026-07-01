TABLE_NAME = "hospitals"

AVAILABLE_COLUMNS = [
    "id",
    "name",
    "name_bangla",
    "code",
    "agency",
    "type",
    "division",
    "district",
    "city_corporation",
    "upazila",
    "paurasava",
    "union",
    "private",
]

HOSPITAL_SCHEMA = f"""
You are generating SQL for SQLite.

Table Name:
{TABLE_NAME}

Available Columns:
{chr(10).join(f"- {c}" for c in AVAILABLE_COLUMNS)}

Rules:
1. Use only these columns.
2. Never invent columns.
3. Generate valid SQLite SQL.
4. Return only SQL.
5. If the user asks:
    - how many
    - number of
    - total hospitals
    - count

    Generate SQL using

    SELECT COUNT(*)

    Never list hospital names for counting questions.
    Examples

    Question:
    How many hospitals are in Dhaka?

    SQL:
    SELECT COUNT(*)
    FROM hospitals
    WHERE division='Dhaka';
"""