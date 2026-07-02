from app.agent import agent_executor

question = input("Ask: ")

response = agent_executor.invoke(
    {
        "input": question
    }
)
print("="*100)
print("\nAnswer\n")
print(response["output"])
print("="*100)