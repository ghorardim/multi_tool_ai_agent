from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from app.schemas.hospital_schema import HOSPITAL_SCHEMA

from app.database.db_loader import get_database
from app.llm import llm


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
        Question
            ↓
        SQL
            ↓
        Execute SQL
            ↓
        Natural Language
        """

        full_question = f"""
        {HOSPITAL_SCHEMA}

        User Question:
        {question}
        """

        # Step 1: Generate SQL
        sql_query = self.sql_chain.invoke(
            {
                "question": full_question
            }
        )

        print("\nGenerated SQL")
        print(sql_query)

        # Step 2: Execute SQL
        sql_result = self.sql_executor.invoke(sql_query)

        print("\nSQL Result")
        print(sql_result)

        # Step 3: Convert to Natural Language

        prompt = ChatPromptTemplate.from_template(
            """
            You are an assistant for Bangladesh hospital data.
            
            The user asked:

            {question}

            The SQL query returned:

            {result}

            Write a concise, natural-language answer.

            If there are multiple rows, format them as a readable list.

            Do NOT mention SQL.
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