from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

from app.database.db_loader import get_database
from app.llm import llm
from app.schemas.hospital_schema import HOSPITAL_SCHEMA

from app.utils.sql_utils import clean_sql
from app.utils.location_keywords import LOCATION_KEYWORDS
from app.utils.keyword_expander import expand_keywords


class HospitalService:
    """
    Handles all interactions with the hospitals database.
    """

    def __init__(self):
        self.db = get_database("hospitals.db")

        self.sql_chain = create_sql_query_chain(
            llm=llm,
            db=self.db,
        )

        self.sql_executor = QuerySQLDatabaseTool(
            db=self.db
        )

    def run(self, question: str) -> str:
        """
        User Question
              ↓
        Expand location keywords
              ↓
        Generate SQL
              ↓
        Execute SQL
              ↓
        Convert Result to Natural Language
        """

        # Expand English/Bangla location names
        location_instruction = expand_keywords(
            question=question,
            keyword_map=LOCATION_KEYWORDS,
            search_target="""
                        Hospital location columns:
                        - division
                        - district
                        - city_corporation
                        - upazila
                        - paurasava
                        - union
                        """,
        )

        full_question = f"""
                        {HOSPITAL_SCHEMA}

                        {location_instruction}
                        """

        # Step 1: Generate SQL
        sql_query = self.sql_chain.invoke(
            {
                "question": full_question
            }
        )

        sql_query = clean_sql(sql_query)

        print("\nGenerated SQL")
        print(sql_query)

        # Step 2: Execute SQL
        sql_result = self.sql_executor.invoke(sql_query)

        print("\nSQL Result")
        print(sql_result)

        # Step 3: Convert SQL result to natural language

        prompt = ChatPromptTemplate.from_template(
            """
                You are an assistant for Bangladesh hospital information.

                User Question:
                {question}

                SQL Result:
                {result}

                Write a concise, natural-language answer.

                Rules:
                - Answer ONLY using the SQL Result.
                - Do NOT use outside knowledge.
                - Do NOT guess or speculate.
                - If the SQL Result contains COUNT(*), answer using that count.
                - If multiple hospitals are returned, present them as a numbered list.
                - Include the hospital name.
                - Include the Bangla name if available.
                - Include the hospital type if available.
                - Include the agency if available.
                - Include the location (division, district, upazila, or city corporation) whenever available.
                - If the hospital is private, show "Private".
                - If the hospital is government, show "Government".
                - Do NOT mention SQL.
                - If the SQL Result is empty ([]), respond exactly:

                "No matching hospitals were found in the hospital database."

                - Do NOT invent hospitals.
                - Do NOT invent locations, agencies, or hospital types.
                - Do NOT suggest searching the web or another database.
            """         
        )

        chain = prompt | llm

        response = chain.invoke(
            {
                "question": question,
                "result": sql_result,
            }
        )

        return response.content