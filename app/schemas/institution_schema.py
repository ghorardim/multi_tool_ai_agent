TABLE_NAME = "institutions"

AVAILABLE_COLUMNS = [
    "institute_name",
    "eiin",
    "institute_type",
    "division_id",
    "division",
    "district_id",
    "district",
    "thana_id",
    "thana",
    "union_id",
    "union_name",
    "mauza_id",
    "mauza_name",
    "area_status",
    "geogrpycal_status",
    "address",
    "post",
    "management_type",
    "mobile",
    "student_type",
    "education_level",
    "affiliation",
    "mpo_status",
]

INSTITUTION_SCHEMA = f"""
You are generating SQL queries for a SQLite database.

Database Information
--------------------
Database Name: institutions.db

Table Name:
- {TABLE_NAME}

Available Columns:
{chr(10).join(f"- {column}" for column in AVAILABLE_COLUMNS)}

Rules:
1. Use ONLY the columns listed above.
2. Never invent column names.
3. Never reference columns that do not exist.
4. If the requested information is unavailable in this database,
   clearly state that it is unavailable.
5. Generate valid SQLite SQL.
6. Return ONLY the SQL query.
"""