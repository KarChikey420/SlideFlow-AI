# from langchain.tools import tool
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# UNSPLASH_API_KEY =os.getenv("access_key")

# if not UNSPLASH_API_KEY:
#     raise ValueError("Missing UNSPLASH_API_KEY in .env file")


# @tool("fetch_image_from_unsplash", return_direct=True)
# def fetch_image_from_unsplash(query: str) -> str:
#     """Fetch an image URL from Unsplash based on a search query."""
#     try:
#         url = (
#             "https://api.unsplash.com/search/photos"
#             f"?query={query}&client_id={UNSPLASH_API_KEY}&per_page=1"
#         )

#         response = requests.get(url, timeout=7)
#         response.raise_for_status()  

#         data = response.json()
#         if data.get("results"):
#             return data["results"][0]["urls"]["regular"]

#         return "No image found for this query."

#     except requests.exceptions.Timeout:
#         return "Image fetch timeout from Unsplash API."

#     except requests.exceptions.RequestException as e:
#         return f"Error fetching image: {str(e)}"

# unsplash.py
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
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
        return "No relevant image found on Unsplash."
    except Exception as e:
        return f"Error fetching image: {str(e)}"