from langchain_core.prompts import PromptTemplate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kimi import kimi_llm


presentation_prompt = PromptTemplate(
    input_variables=["topic", "slide_count"],
    template=(
        "You are an expert presentation designer.\n"
        "Generate structured content for a presentation on the topic: **{topic}**.\n"
        "Create exactly {slide_count} slides.\n\n"
        "For each slide, strictly follow this format:\n\n"
        "Slide X:\n"
        "<title>\n" 
        "<bullet_point_1>\n"
        "<bullet_point_2>\n"
        "<bullet_point_3>\n"
        "Image Query: <short image keyword for Unsplash>\n\n"
        "Rules:\n"
        "- No markdown\n"
        "- No numbering or dashes before bullets\n"
        "- Image Query should be SHORT (max 4 words), relevant to slide\n"
        "- Only single line for Image Query\n\n"
        "Now generate the presentation content:"
    )
)

def generate_presentation_content(topic: str, slide_count: int = 10) -> str:
    try:
        prompt = presentation_prompt.format(topic=topic, slide_count=slide_count)
        result = kimi_llm.invoke(prompt)
        return result.content
    except Exception as e:
        return f"Error generating presentation: {str(e)}"


