from langchain.agents import initialize_agent, AgentType
from app.kimi import kimi_llm
from app.unplash import fetch_image_from_unsplash

tools = [fetch_image_from_unsplash]

agent = initialize_agent(
    tools=tools,
    llm=kimi_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
