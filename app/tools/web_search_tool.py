from langchain.tools import tool
from ddgs import DDGS
from langchain_core.prompts import ChatPromptTemplate

from app.llm import llm


@tool
def web_search_tool(question: str) -> str:
    """
    Use this tool ONLY for questions that cannot be answered
    using the local databases.

    Examples:
    - government policies
    - healthcare policy
    - Bangladesh history
    - current events
    - definitions
    - general knowledge
    """

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    question,
                    max_results=5,
                )
            )

        if not results:
            return "No relevant web search results were found."

        formatted_results = "\n\n".join(
            [
                f"Title: {r.get('title', '')}\n"
                f"Body: {r.get('body', '')}\n"
                f"URL: {r.get('href', '')}"
                for r in results
            ]
        )

    except Exception as e:
        return f"Web search failed: {e}"

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert assistant.

        Answer ONLY using the web search results below.

        User Question:
        {question}

        Web Search Results:
        {results}

        Rules:

        - Give a direct answer.
        - If multiple sources agree, combine the information.
        - If appropriate, use bullet points.
        - Do NOT mention DuckDuckGo.
        - Do NOT mention that a search was performed.
        - If the search results truly do not contain the answer, clearly say that.
        - Do NOT invent facts.
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "results": formatted_results,
        }
    )

    return response.content