from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

from app.database.db_loader import get_database
from app.llm import llm
from app.schemas.institution_schema import INSTITUTION_SCHEMA

from app.utils.sql_utils import clean_sql
from app.utils.location_keywords import LOCATION_KEYWORDS
from app.utils.keyword_expander import expand_keywords


class InstitutionService:
    """
    Handles all interactions with the institutions database.
    """

    def __init__(self):
        self.db = get_database("institutions.db")

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
                            Institution location columns:
                            - division
                            - district
                            - thana
                            - union_name
                            - mauza_name
                            - address
                            - post
                            """,
        )

        full_question = f"""
                        {INSTITUTION_SCHEMA}

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
            You are an assistant for Bangladesh educational institution information.

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
            - If multiple institutions are returned, present them as a numbered list.
            - Include the institute name.
            - Include the institute type if available.
            - Include the EIIN if available.
            - Include the address if available.
            - Do NOT mention SQL.
            - If the SQL Result is empty ([]), respond exactly:

                "No matching records were found in the institutions database."

            - Do NOT say the institution does not exist.
            - Do NOT say Bangladesh has no such university.
            - Do NOT suggest web search or other databases.
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