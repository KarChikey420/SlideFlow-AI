# presentation_chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from llm import llm
import json

# FIXED PROMPT (all JSON braces escaped)
prompt = ChatPromptTemplate.from_template("""
You are an expert presentation designer.

Create a presentation outline on the topic: "{topic}"

Generate exactly {slide_count} slides.

Return the output ONLY as a JSON list.
Each slide must have this structure:

{{
  "title": "...",
  "content": "...",
  "image_query": "..."
}}

Rules:
- Keep titles short & clear.
- Content must be 3–5 bullet points.
- image_query must be a short phrase ideal for Unsplash.
- Do NOT include markdown or explanations.
- Return ONLY valid JSON.
""")

presentation_chain = RunnableSequence(prompt, llm)


def generate_slides(topic: str, slide_count: int = 6):
    result = presentation_chain.invoke({
        "topic": topic,
        "slide_count": slide_count
    })

    try:
        slides = json.loads(result.content)
    except Exception as e:
        raise ValueError("LLM did not return valid JSON:\n" + result.content)

    return slides


if __name__ == "__main__":
    topic = "Artificial Intelligence in Healthcare"
    slides = generate_slides(topic, slide_count=5)

    print("\nGenerated Slides:\n")
    for s in slides:
        print(s, "\n")
