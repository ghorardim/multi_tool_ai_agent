from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate

from app.llm import llm

search = DuckDuckGoSearchRun()


@tool
def web_search_tool(question: str) -> str:
    """
    Use this tool ONLY for general knowledge questions.
    """

    search_result = search.run(question)

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful AI assistant.

        User Question:
        {question}

        Search Result:
        {result}

        Write a concise and accurate answer based on the search result.
        Do not mention DuckDuckGo or that a search was performed.
        If the search result is insufficient, say so politely.
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "result": search_result,
        }
    )

    return response.content