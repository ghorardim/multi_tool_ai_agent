from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from app.utils.food_keywords import FOOD_KEYWORDS

from app.database.db_loader import get_database
from app.llm import llm
from app.schemas.restaurant_schema import RESTAURANT_SCHEMA
import re


class RestaurantService:
    """
    Handles all interactions with the restaurants database.
    """

    def __init__(self):
        self.db = get_database("restaurants.db")

        self.sql_chain = create_sql_query_chain(
            llm=llm,
            db=self.db,
        )

        self.sql_executor = QuerySQLDatabaseTool(
            db=self.db
        )

    def _expand_food_keywords(self, question: str) -> str:
        """
        Expand food keywords into their English and Bangla variants
        to help the LLM generate better SQL.
        """

        lower_question = question.lower()

        matched_variants = []

        for keyword, variants in FOOD_KEYWORDS.items():
            if re.search(rf"\b{re.escape(keyword)}\b", lower_question):
                matched_variants.extend(variants)

            # Remove duplicates while preserving order
            matched_variants = list(dict.fromkeys(matched_variants))

            if not matched_variants:
                return f"""
        User Question:
        {question}
        """

        variants_text = ", ".join(matched_variants)

        return f"""
            User Question:
            {question}

            IMPORTANT:

            When searching the restaurant name column,
            treat the following keywords as equivalent:

            {variants_text}

            Generate SQL that searches for ALL of these keywords
            using SQLite LIKE conditions.
            """
    
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

        expanded_question = self._expand_food_keywords(question)

        full_question = f"""
                        {RESTAURANT_SCHEMA}

                        {expanded_question}
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

        # Step 3: Convert SQL result to natural language
        prompt = ChatPromptTemplate.from_template(
            """
            You are an assistant for Bangladesh restaurant information.

            User Question:
            {question}

            SQL Result:
            {result}

            Write a concise, natural-language answer.

            Rules:
            - If multiple restaurants are returned, present them as a numbered list.
            - Include the restaurant name, rating (if available), and address.
            - Do NOT mention SQL.
            - If no restaurants are found, clearly state that.
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