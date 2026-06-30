from langchain.tools import tool

from app.services.institution_service import InstitutionService


institution_service = InstitutionService()


@tool
def institutions_db_tool(question: str) -> str:
    """
    Use this tool ONLY for questions related to educational
    institutions in Bangladesh.

    Examples:
    - Schools
    - Colleges
    - Madrasas
    - Institutes
    - EIIN
    - MPO status
    - Education level
    - Affiliation
    - Management type
    - Student type
    - District
    - Division
    - Thana
    - Union
    - Address
    """

    return institution_service.run(question)