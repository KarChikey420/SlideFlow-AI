from kimi import kimi_llm
from unplash import fetch_image_from_unsplash
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
import json

@tool
def fetch_image(query: str) -> str:
    """Fetches an image from Unsplash based on a search query."""
    return fetch_image_from_unsplash(query)

tools = [fetch_image]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(kimi_llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def generate_full_presentation(topic: str, slide_count: int = 10):
    prompt_text = f"""
You are a slide presentation generator.

Create a {slide_count}-slide presentation on the topic: "{topic}".

For each slide return:
- slide_number
- title
- content (3–5 bullet points)
- image_query (short keyword)

Output the result ONLY in valid JSON array format.
Without explanation.
"""

    response = agent_executor.invoke({"input": prompt_text})
    try:
        slides = json.loads(response["output"])
        return slides
    except Exception as e:
        return {"error": f"Failed to parse JSON: {str(e)}", "raw": response["output"]}

if __name__ == "__main__":
    topic = "ai in health care"
    result = generate_full_presentation(topic, 5)
    print(json.dumps(result, indent=2))