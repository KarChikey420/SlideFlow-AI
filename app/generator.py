import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import AIMessage, ToolMessage

from llm import llm
from unplash import fetch_image_from_unsplash


slide_prompt = ChatPromptTemplate.from_template("""
You are an expert presentation designer.

Create a presentation outline on the topic: "{topic}"

Generate exactly {slide_count} slides.

Return ONLY valid JSON: a list of objects.

Each slide should look like:

{{
  "title": "...",
  "content": "...",
  "image_query": "..."
}}

Rules:
- Title must be short.
- Content must be 5 bullet points.
- image_query = short phrase ideal for Unsplash.
- No markdown.
- No explanations.
""")

slide_chain = RunnableSequence(slide_prompt, llm)


def generate_slides(topic: str, slide_count: int = 10):
    """Generates slide blueprint with titles, text, and image query."""

    result = slide_chain.invoke({
        "topic": topic,
        "slide_count": slide_count
    })

    try:
        slides = json.loads(result.content)
    except Exception:
        raise ValueError("LLM did not return valid JSON:\n" + result.content)

    return slides

llm_with_tools = llm.bind_tools([fetch_image_from_unsplash])

image_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You generate image URLs based on given search queries."),
        MessagesPlaceholder("messages"),
    ]
)

image_agent = RunnableSequence(image_prompt, llm_with_tools)


def execute_tool(tool_call):
    """Run the actual tool."""
    if tool_call["name"] == "fetch_image_from_unsplash":
        return fetch_image_from_unsplash.run(tool_call["args"]["query"])


def get_image_url(query: str):
    """Fetches image URL using tool calling agent."""

    messages = [("human", f"Fetch an image for: {query}")]

    response1 = image_agent.invoke({"messages": messages})

    ai_msg = AIMessage(
        content=response1.content,
        tool_calls=response1.tool_calls
    )
    messages.append(ai_msg)

    if response1.tool_calls:

        for call in response1.tool_calls:
            result = execute_tool(call)

            tool_msg = ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
            messages.append(tool_msg)

        response2 = image_agent.invoke({"messages": messages})

        return result 

    return None

def create_presentation(topic: str, slide_count: int = 10):
    slides = generate_slides(topic, slide_count)

    final_slides = []

    for slide in slides:
        image_query = slide.get("image_query", "")
        image_url = get_image_url(image_query)

        slide["image_url"] = image_url
        final_slides.append(slide)

    return final_slides

