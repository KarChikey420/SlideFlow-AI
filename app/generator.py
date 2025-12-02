from kimi import kimi_llm
from unplash import fetch_image_from_unsplash

try:
    from langchain.agents import create_react_agent
except ImportError:
    from langgraph.prebuilt import create_react_agent

tools = [fetch_image_from_unsplash]

agent_executor = create_react_agent(
    model=kimi_llm,
    tools=tools
)

def generate_full_presentation(topic: str, slide_count: int = 10):
    system_message = f"""
    You are an expert PPT generator. Be CONCISE.

    You MUST:
    - Generate EXACTLY {slide_count} slides.
    - For each slide return:
       {{"title": "...", "bullets": ["1","2","3","4","5"], "img_query": "..."}}
    - THEN, for each img_query, call fetch_image_from_unsplash.
    - Add "image_url" to each slide JSON.
    - Final output: JSON list of slides with image URLs.
    
    Keep responses SHORT to save tokens.
    """
    
    result = agent_executor.invoke({
        "messages": [
            ("system", system_message),
            ("user", f"Create a presentation on: {topic}")
        ]
    })
    
    return result

if __name__ == "__main__":
    topic = "The Future of Artificial Intelligence"
    presentation = generate_full_presentation(topic, slide_count=5)  
    print(presentation)
