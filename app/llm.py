
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI

load_dotenv()

#token = os.getenv("GITHUB_TOKEN")
#print(token[:10] + "..." if token else "No token found")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
    temperature=0,
)

#---------------------------------------------#

# from langchain_ollama import ChatOllama

# llm = ChatOllama(
#     model="qwen2.5:3b",
#     temperature=0,
# )