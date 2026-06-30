from langchain.tools import tool

from app.services.restaurant_service import RestaurantService


restaurant_service = RestaurantService()


@tool
def restaurants_db_tool(question: str) -> str:
    """
    Use this tool ONLY for questions about restaurants in Bangladesh.

    Examples:
    - Restaurants in Dhaka
    - Restaurants in Chattogram
    - Top rated restaurants
    - Restaurant ratings
    - Number of reviews
    - Restaurant addresses
    - Popular restaurants
    - Affluence score
    """

    return restaurant_service.run(question)