from app.tools.hospital_tool import hospitals_db_tool


question = "How many hospitals are in Dhaka district?"

response = hospitals_db_tool.invoke(
    {
        "question": question
    }
)

print("\nAnswer\n")
print(response)