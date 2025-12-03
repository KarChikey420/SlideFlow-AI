from kimi import kimi_llm
from unplash import fetch_image_from_unsplash
import json
import re

def generate_full_presentation(topic: str, slide_count: int = 10):
    """Generate a complete presentation with slides and images."""
    
    prompt = f"""
You are a slide presentation generator.

Create a {slide_count}-slide presentation on the topic: "{topic}".

For each slide return:
- slide_number (integer)
- title (string)
- content (array of 3-5 bullet points)
- image_query (short keyword for image search)

Output the result ONLY in valid JSON array format like this:
[
  {{
    "slide_number": 1,
    "title": "",
    "content": [],
    "image_query": ""
  }}
]

Do not include any explanation, preamble, or markdown formatting. Just the JSON array.
"""

    try:
        print(f"Generating {slide_count} slides on '{topic}'...")
        response = kimi_llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            content = response.content
        elif isinstance(response, dict) and 'content' in response:
            content = response['content']
        else:
            content = str(response)
        
        print("LLM response received, parsing...")
        
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        content = content.strip()
        
        slides = json.loads(content)
        print(f"Successfully parsed {len(slides)} slides")
        
        print("\nFetching images from Unsplash...")
        for i, slide in enumerate(slides, 1):
            if 'image_query' in slide:
                try:
                    print(f"  [{i}/{len(slides)}] Fetching: '{slide['image_query']}'")
                    slide['image_url'] = fetch_image_from_unsplash(slide['image_query'])
                    print(f"Success")
                except Exception as img_error:
                    slide['image_url'] = None
                    print(f"Failed: {img_error}")
        
        return slides
        
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON parsing error: {e}")
        print(f"Content received:\n{content if 'content' in locals() else 'N/A'}")
        return {
            "error": f"JSON parsing failed: {str(e)}", 
            "raw": content if 'content' in locals() else "No content"
        }
    except Exception as e:
        print(f"\nError: {e}")
        return {
            "error": f"Generation failed: {str(e)}", 
            "raw": str(e)
        }

if __name__ == "__main__":
    topic = "ai in health care"
    print("="*60)
    print(f"PRESENTATION GENERATOR")
    print("="*60)
    
    result = generate_full_presentation(topic, 10)
    
    print("\n" + "="*60)
    if "error" in result:
        print("❌ ERROR OCCURRED")
        print("="*60)
        print(json.dumps(result, indent=2))
    else:
        print("✓ PRESENTATION GENERATED SUCCESSFULLY")
        print("="*60)
        print(json.dumps(result, indent=2))