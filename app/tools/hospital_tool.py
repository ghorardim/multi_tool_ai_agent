from langchain.tools import tool

from app.services.hospital_service import HospitalService


hospital_service = HospitalService()


@tool
def hospitals_db_tool(question: str) -> str:
    """
    Answers questions using the Bangladesh hospitals SQLite database.

    Use this tool for ANY question about hospitals, including:
    - number of hospitals
    - hospital count
    - hospitals in a division
    - hospitals in a district
    - hospitals in an upazila
    - government hospitals
    - private hospitals
    - hospital agency
    - hospital type
    - hospital code
    - hospital location
    - city corporation
    - union
    - hospital statistics

    This tool should always be used before using WebSearchTool for hospital-related questions.

    Input:
        A user's natural language question.

    Output:
        A natural-language answer generated from the hospitals database.
    """

    return hospital_service.run(question)