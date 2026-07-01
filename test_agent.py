from app.agent import agent_executor

question = input("Ask: ")

response = agent_executor.invoke(
    {
        "input": question
    }
)

print("\nAnswer\n")
print(response["output"])