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

# from kimi import kimi_llm
# from unplash import fetch_image_from_unsplash
# import json
# import re

# try:
#     from langchain.agents import create_react_agent
# except ImportError:
#     from langgraph.prebuilt import create_react_agent

# tools = [fetch_image_from_unsplash]

# agent_executor = create_react_agent(
#     model=kimi_llm,
#     tools=tools
# )

# def generate_full_presentation(topic: str, slide_count: int = 10):
#     system_message = f"""You are an expert PPT generator.

# CRITICAL INSTRUCTIONS:
# 1. First, create {slide_count} slides with titles and bullet points
# 2. Then call fetch_image_from_unsplash for EACH slide's img_query
# 3. Finally, return the complete JSON with all image URLs included

# Output format (return this exact JSON structure):
# [
#   {{
#     "title": "Slide Title Here",
#     "bullets": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
#     "img_query": "search term for image",
#     "image_url": "URL_FROM_TOOL"
#   }},
#   ...
# ]

# After calling all tools, YOU MUST return the final complete JSON array with all {slide_count} slides.
# """
    
#     result = agent_executor.invoke({
#         "messages": [
#             ("system", system_message),
#             ("user", f"Create a {slide_count}-slide presentation on: {topic}")
#         ]
#     })
    
#     return result

# def extract_slides_from_messages(result):
#     """
#     Parse the agent messages to extract slides and match them with fetched images.
#     """
#     if not isinstance(result, dict) or "messages" not in result:
#         return None
    
#     messages = result["messages"]
    
#     # Extract image URLs from ToolMessages
#     image_urls = []
#     for msg in messages:
#         if hasattr(msg, '__class__') and msg.__class__.__name__ == 'ToolMessage':
#             if hasattr(msg, 'content'):
#                 image_urls.append(msg.content)
    
#     # Try to find AI message with JSON
#     for msg in reversed(messages):
#         if hasattr(msg, '__class__') and msg.__class__.__name__ == 'AIMessage':
#             if hasattr(msg, 'content'):
#                 content = msg.content
                
#                 # Try to parse JSON from content
#                 try:
#                     # Direct JSON parse
#                     slides = json.loads(content)
#                     if isinstance(slides, list):
#                         return slides
#                 except:
#                     pass
                
#                 # Try to extract JSON array
#                 match = re.search(r'\[[\s\S]*\]', content)
#                 if match:
#                     try:
#                         slides = json.loads(match.group(0))
#                         if isinstance(slides, list):
#                             return slides
#                     except:
#                         pass
    
#     # If no JSON found, construct slides from image URLs
#     if image_urls:
#         print(f"⚠️  Agent didn't return slide content. Creating basic structure with {len(image_urls)} images...")
#         # We'll need to make a follow-up call or construct manually
#         return None
    
#     return None

# def create_presentation_with_retry(topic: str, slide_count: int = 5):
#     """
#     Generate presentation with better prompt and fallback logic.
#     """
#     print(f"🎯 Generating presentation on: {topic}")
#     print("⏳ Step 1: Fetching images...")
    
#     # First, get the agent to fetch images
#     result = generate_full_presentation(topic, slide_count)
    
#     # Extract image URLs from tool messages
#     image_urls = []
#     if isinstance(result, dict) and "messages" in result:
#         for msg in result["messages"]:
#             if hasattr(msg, '__class__') and msg.__class__.__name__ == 'ToolMessage':
#                 if hasattr(msg, 'content'):
#                     image_urls.append(msg.content)
    
#     print(f"✓ Fetched {len(image_urls)} images")
    
#     # Check if we got slide content
#     slides = extract_slides_from_messages(result)
    
#     if slides and isinstance(slides, list) and len(slides) > 0:
#         print(f"✓ Generated {len(slides)} slides with content")
#         return slides
    
#     # Fallback: Make a direct LLM call to generate slide content
#     print("⏳ Step 2: Generating slide content...")
    
#     prompt = f"""Create a {slide_count}-slide presentation on: {topic}

# Return ONLY a JSON array with this exact structure (no markdown, no extra text):
# [
#   {{
#     "title": "Introduction to AI",
#     "bullets": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
#     "img_query": "artificial intelligence technology"
#   }},
#   ...
# ]

# Generate exactly {slide_count} slides."""
    
#     from langchain_core.messages import HumanMessage
#     response = kimi_llm.invoke([HumanMessage(content=prompt)])
    
#     try:
#         content = response.content.strip()
        
#         # Remove markdown code blocks
#         if content.startswith("```"):
#             content = re.sub(r'^```(?:json)?\s*\n?', '', content)
#             content = re.sub(r'\n?```\s*$', '', content)
        
#         slides = json.loads(content.strip())
        
#         # Add image URLs to slides
#         for i, slide in enumerate(slides):
#             if i < len(image_urls):
#                 slide["image_url"] = image_urls[i]
#             else:
#                 slide["image_url"] = None
        
#         print(f"✓ Generated {len(slides)} slides")
#         return slides
        
#     except Exception as e:
#         print(f"❌ Error parsing slides: {e}")
        
#         # Last resort: create basic structure
#         slides = []
#         for i in range(min(slide_count, len(image_urls))):
#             slides.append({
#                 "title": f"Slide {i+1}: {topic}",
#                 "bullets": [
#                     "Key point 1",
#                     "Key point 2", 
#                     "Key point 3",
#                     "Key point 4",
#                     "Key point 5"
#                 ],
#                 "img_query": f"{topic} slide {i+1}",
#                 "image_url": image_urls[i]
#             })
        
#         return slides

# def save_presentation_json(slides, filename="presentation.json"):
#     """
#     Save slides to JSON file.
#     """
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(slides, f, indent=2, ensure_ascii=False)
    
#     print(f"\n✓ Saved JSON → {filename}")
#     return slides

# if __name__ == "__main__":
#     topic = "The Future of Artificial Intelligence"
    
#     slides = create_presentation_with_retry(topic, slide_count=5)
    
#     # Save and display
#     save_presentation_json(slides, filename="presentation.json")
    
#     print("\n" + "="*60)
#     print(f"📊 GENERATED {len(slides)} SLIDES")
#     print("="*60)
    
#     for i, slide in enumerate(slides, 1):
#         print(f"\n📄 Slide {i}: {slide.get('title', 'N/A')}")
#         bullets = slide.get('bullets', [])
#         for bullet in bullets:
#             print(f"   • {bullet}")
#         print(f"   🖼️  Image: {slide.get('image_url', 'N/A')[:80]}...")