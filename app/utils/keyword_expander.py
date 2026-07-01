import re


def expand_keywords(question: str, keyword_map: dict, search_target: str) -> str:
    """
    Expand keywords (food, location, etc.) into their English and Bangla variants
    to help the LLM generate better SQL.
    """

    lower_question = question.lower()
    matched_variants = []

    for keyword, variants in keyword_map.items():
        if re.search(rf"\b{re.escape(keyword)}\b", lower_question):
            matched_variants.extend(variants)

    # Remove duplicates while preserving order
    matched_variants = list(dict.fromkeys(matched_variants))

    if not matched_variants:
        return ""

    variants_text = ", ".join(matched_variants)

    return f"""
            IMPORTANT:

            When searching the {search_target} column,
            treat the following keywords as equivalent:

            {variants_text}

            Generate SQL that searches for ALL of these keywords
            using SQLite LIKE conditions.
            """