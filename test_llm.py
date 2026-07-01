from app.llm import llm

response = llm.invoke("What is the capital of Bangladesh?")

print(response.content)