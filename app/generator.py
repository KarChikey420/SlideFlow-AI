from kimi import kimi_llm
from unplash import fetch_image_from_unsplash
import json

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

def save_presentation_json(result, filename="presentation.json"):
    """
    Extract JSON list from agent response and save it cleanly.
    """

    # LangChain may return dict, string, or structured output
    # We try to normalize it.

    if isinstance(result, list):
        slides = result

    elif isinstance(result, dict):

        # look for common keys
        for key in ["output", "text", "result", "response"]:
            if key in result and isinstance(result[key], str):
                try:
                    slides = json.loads(result[key])
                    break
                except:
                    continue
        else:
            slides = result  # assume it is already JSON-like

    elif isinstance(result, str):
        try:
            slides = json.loads(result)
        except:
            # strip loose text around JSON
            import re
            m = re.search(r"(\[.*\])", result, re.S)
            slides = json.loads(m.group(1)) if m else {"raw": result}

    else:
        slides = {"raw": str(result)}

    # Save file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(slides, f, indent=2, ensure_ascii=False)

    print(f"Saved JSON → {filename}")
    return filename

if __name__ == "__main__":
    topic = "The Future of Artificial Intelligence"
    presentation = generate_full_presentation(topic, slide_count=5) 
    save_presentation_json(presentation, filename="presentation.json") 

