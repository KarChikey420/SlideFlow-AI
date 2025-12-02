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

    You MUST follow these steps:
    1. Generate EXACTLY {slide_count} slides with this structure:
       {{"title": "...", "bullets": ["1","2","3","4","5"], "img_query": "..."}}
    
    2. For EACH slide, you MUST call the fetch_image_from_unsplash tool with the img_query.
    
    3. After getting the image URL from the tool, replace "img_query" with "image_url" in that slide.
    
    4. Final output must be a JSON list where each slide has "image_url" (NOT "img_query").
    
    IMPORTANT: You must use the fetch_image_from_unsplash tool {slide_count} times, once for each slide.
    
    Keep responses SHORT to save tokens.
    """
    
    result = agent_executor.invoke({
        "messages": [
            ("system", system_message),
            ("user", f"Create a presentation on: {topic}. You MUST fetch images using the tool for ALL {slide_count} slides.")
        ]
    })
    
    slides = extract_and_fix_slides(result)
    
    result['slides'] = slides
    
    return result


def extract_and_fix_slides(result):
    """Extract slides and fetch images if missing"""
    try:
        if 'messages' not in result:
            return []
        
        from langchain_core.messages import AIMessage
        
        ai_messages = [msg for msg in result['messages'] if isinstance(msg, AIMessage)]
        
        if not ai_messages:
            print("No AI messages found in result")
            return []
        
        slides = None
        for msg in reversed(ai_messages):
            try:
                content = msg.content if hasattr(msg, 'content') else str(msg)
                content = content.strip()
                
                if content.startswith('```'):
                    lines = content.split('\n')
                    content = '\n'.join(lines[1:-1]) if len(lines) > 2 else content
                
                parsed = json.loads(content)
                
                if isinstance(parsed, list) and len(parsed) > 0:
                    if 'title' in parsed[0]:
                        slides = parsed
                        break
                elif isinstance(parsed, dict) and 'title' in parsed:
                    slides = [parsed]
                    break
            except:
                continue
        
        if not slides:
            print("Could not find slide data in any AI message")
            return []
        
        needs_images = any('img_query' in slide and 'image_url' not in slide for slide in slides)
        
        if needs_images:
            print("⚠️  Agent didn't fetch images. Fetching them now...")
            for i, slide in enumerate(slides, 1):
                if 'img_query' in slide:
                    try:
                        query = slide['img_query']
                        print(f"  🔍 [{i}/{len(slides)}] Fetching: {query}")
                        
                        image_url = fetch_image_from_unsplash.invoke({"query": query})
                        
                        slide['image_url'] = image_url
                        del slide['img_query']
                        print(f"Success")
                    except Exception as e:
                        print(f"Failed: {e}")
                        slide['image_url'] = None
                        if 'img_query' in slide:
                            del slide['img_query']
        
        return slides
        
    except Exception as e:
        print(f"Error processing slides: {e}")
        import traceback
        traceback.print_exc()
        return []