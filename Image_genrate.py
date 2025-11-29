import os, requests
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("access_key")

def get_image(q):
    r = requests.get(f"https://api.unsplash.com/search/photos?query={q}&client_id={API}&per_page=1").json()
    return r["results"][0]["urls"]["regular"] if r.get("results") else None

img_url = get_image("AI healthcare technology")
print(img_url)
