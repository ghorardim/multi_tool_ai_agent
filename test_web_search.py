from app.tools.web_search_tool import web_search_tool

question = "What is the healthcare policy of Bangladesh?"

response = web_search_tool.invoke(
    {
        "question": question
    }
)

print(response)