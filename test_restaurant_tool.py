from app.tools.restaurant_tool import restaurants_db_tool

question = "Find restaurants in Chattogram serving biryani."

response = restaurants_db_tool.invoke(
    {
        "question": question
    }
)

print("\nAnswer\n")
print(response)