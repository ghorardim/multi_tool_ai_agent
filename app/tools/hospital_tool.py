from langchain.tools import tool

from app.services.hospital_service import HospitalService


hospital_service = HospitalService()


@tool
def hospitals_db_tool(question: str) -> str:
    """
    Use this tool ONLY for questions related to
    hospitals in Bangladesh.

    Examples:
    - hospitals in Dhaka
    - hospitals in Rajshahi
    - private hospitals
    - government hospitals
    - hospital codes
    - agencies
    - divisions
    - districts
    - upazilas
    - unions
    - city corporations
    """

    return hospital_service.run(question)