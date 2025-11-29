from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def fetch_image_from_unsplash(query: str) -> str:
    """Fetch relevant image URL from Unsplash API using search query."""
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={os.getenv('access_key')}&per_page=1"
    response = requests.get(url).json()
    if response.get("results"):
        return response["results"][0]["urls"]["regular"]
    return "No image found"
