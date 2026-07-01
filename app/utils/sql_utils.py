import re


def clean_sql(sql: str) -> str:
    sql = sql.strip()

    sql = re.sub(r"^SQLQuery\s*:\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```", "", sql)
    sql = sql.replace("```", "")

    return sql.strip()