from app.tools.institution_tool import institutions_db_tool

question = "List 5 colleges in Dhaka."

response = institutions_db_tool.invoke(
    {
        "question": question
    }
)

print("\nAnswer\n")
print(response)