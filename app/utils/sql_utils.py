import re

from app.utils.location_keywords import LOCATION_KEYWORDS


def clean_sql(sql: str) -> str:
    sql = sql.strip()

    sql = re.sub(r"^SQLQuery\s*:\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```", "", sql)
    sql = sql.replace("```", "")

    return sql.strip()

def fix_limit(question, sql):

    match = re.search(
        r"(top|first|show)\s+(\d+)",
        question.lower()
    )

    if match:
        wanted = match.group(2)

        if re.search(r"limit\s+\d+", sql, re.I):
            sql = re.sub(
                r"limit\s+\d+",
                f"LIMIT {wanted}",
                sql,
                flags=re.I,
            )
        else:
            sql += f"\nLIMIT {wanted}"

    return sql


LOCATION_COLUMNS = [
    "division",
    "district",
    "city_corporation",
    "upazila",
    "paurasava",
    "union",
]


def adjust_location_filter(sql: str, question: str) -> str:
    """
    Inject a WHERE clause if:
      - the user asked for a location
      - generated SQL has no WHERE clause
    """

    upper_sql = sql.upper()

    if "WHERE" in upper_sql:
        return sql

    location = None

    for english, keywords in LOCATION_KEYWORDS.items():
        if any(k.lower() in question.lower() for k in keywords):
            location = keywords
            break

    if not location:
        return sql

    conditions = []

    for keyword in location:
        for column in LOCATION_COLUMNS:
            conditions.append(f'"{column}" LIKE \'%{keyword}%\'')

    where_clause = "\nWHERE\n    " + "\n OR ".join(conditions)

    sql = re.sub(
        r";\s*$",
        "",
        sql.strip()
    )

    if "LIMIT" in upper_sql:
        sql = re.sub(
            r"\bLIMIT\b",
            where_clause + "\nLIMIT",
            sql,
            flags=re.IGNORECASE,
        )
    else:
        sql += where_clause

    return sql + ";"