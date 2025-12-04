from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")

llm = ChatOpenAI(
    model="openai/gpt-4o",  
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=1400,
)