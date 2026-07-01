from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor

from app.llm import llm

from app.prompts.react_prompt import REACT_PROMPT

from app.tools.hospital_tool import hospitals_db_tool
from app.tools.institution_tool import institutions_db_tool
from app.tools.restaurant_tool import restaurants_db_tool
from app.tools.web_search_tool import web_search_tool

tools = [
    hospitals_db_tool,
    institutions_db_tool,
    restaurants_db_tool,
    web_search_tool,
]

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=REACT_PROMPT,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)