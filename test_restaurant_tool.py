from app.tools.restaurant_tool import restaurants_db_tool

question = "List the top 5 highest rated restaurants."

response = restaurants_db_tool.invoke(
    {
        "question": question
    }
)

print("\nAnswer\n")
print(response)