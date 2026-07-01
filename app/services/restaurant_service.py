from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

from app.database.db_loader import get_database
from app.llm import llm
from app.schemas.restaurant_schema import RESTAURANT_SCHEMA

from app.utils.sql_utils import clean_sql

from app.utils.food_keywords import FOOD_KEYWORDS
from app.utils.location_keywords import LOCATION_KEYWORDS
from app.utils.keyword_expander import expand_keywords


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

    def run(self, question: str) -> str:
        """
        User Question
              ↓
        Expand Keywords
              ↓
        Generate SQL
              ↓
        Execute SQL
              ↓
        Convert Result to Natural Language
        """

        # Food keyword expansion
        food_instruction = expand_keywords(
            question=question,
            keyword_map=FOOD_KEYWORDS,
            search_target="name",
        )

        # Location keyword expansion
        location_instruction = expand_keywords(
            question=question,
            keyword_map=LOCATION_KEYWORDS,
            search_target="address",
        )

        full_question = f"""
                        {RESTAURANT_SCHEMA}

                        {food_instruction}

                        {location_instruction}

                        User Question:
                        {question}
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