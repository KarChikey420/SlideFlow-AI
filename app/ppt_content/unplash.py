from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("access_key")
if not UNSPLASH_ACCESS_KEY:
    raise ValueError("Missing UNSPLASH_ACCESS_KEY in .env")

@tool("fetch_image_from_unsplash")
def fetch_image_from_unsplash(query: str) -> str:
    """Fetch a relevant image URL from Unsplash based on a descriptive query."""
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
        headers = {"User-Agent": "LangChain-App/1.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
        return None
    except Exception as e:
        print(f"Unsplash error: {e}")
        return None