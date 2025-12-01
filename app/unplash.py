from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_API_KEY =os.getenv("access_key")

if not UNSPLASH_API_KEY:
    raise ValueError("Missing UNSPLASH_API_KEY in .env file")


@tool("fetch_image_from_unsplash", return_direct=True)
def fetch_image_from_unsplash(query: str) -> str:
    """Fetch an image URL from Unsplash based on a search query."""
    try:
        url = (
            "https://api.unsplash.com/search/photos"
            f"?query={query}&client_id={UNSPLASH_API_KEY}&per_page=1"
        )

        response = requests.get(url, timeout=7)
        response.raise_for_status()  

        data = response.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]

        return "No image found for this query."

    except requests.exceptions.Timeout:
        return "Image fetch timeout from Unsplash API."

    except requests.exceptions.RequestException as e:
        return f"Error fetching image: {str(e)}"
