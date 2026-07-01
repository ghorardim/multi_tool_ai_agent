from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

from app.database.db_loader import get_database
from app.llm import llm
from app.schemas.institution_schema import INSTITUTION_SCHEMA
from app.utils.sql_utils import clean_sql


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
        Generate SQL
              ↓
        Execute SQL
              ↓
        Convert Result to Natural Language
        """

        full_question = f"""
        {INSTITUTION_SCHEMA}

        User Question:
        {question}
        """

        # Generate SQL
        sql_query = self.sql_chain.invoke(
            {
                "question": full_question
            }
        )
        
        sql_query = clean_sql(sql_query)
        print("\nGenerated SQL")
        print(sql_query)

        # Execute SQL
        sql_result = self.sql_executor.invoke(sql_query)

        print("\nSQL Result")
        print(sql_result)

        # Convert to natural language
        prompt = ChatPromptTemplate.from_template(
            """
            You are an assistant for Bangladesh institutional information.

            User Question:
            {question}

            SQL Result:
            {result}

            Write a concise, natural-language answer.

            If multiple records are returned:
            - Format them as a numbered list.
            - Do NOT mention SQL.
            - If no records are found, say so politely.
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